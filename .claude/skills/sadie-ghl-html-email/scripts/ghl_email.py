"""Helpers for building Sadie's GoHighLevel (GHL) HTML emails.

Import from your own throw-away build script (keep that script outside the repo):

    import sys; sys.path.insert(0, '<skill dir>/scripts')
    from ghl_email import *
    body = (greeting('Hei {{contact.first_name}},') + p('Normal paragraph with **bold**.')
            + cta('Meld deg på her', 'https://example.com') + signature(['Sadie ❤️']))
    write('emails/my-seq/email-01-slug.html',
          assemble(body, subject='...', preheader='...', label='E-POST 1 — DAG 1'))

All text goes in as light markdown: **bold**, *italic*, [text](url), newlines become <br>.
Copy is never reworded; merge fields such as {{contact.first_name}} pass through untouched.
Output is plain UTF-8 (æøå and emoji stay as characters), like Sadie's own GHL emails.
"""
import html
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
TEMPLATE = os.path.join(HERE, '..', 'assets', 'ghl-email-template.html')

PURPLE, MAGENTA = '#5C3884', '#963885'
LINK = 'color:%s; text-decoration:underline;' % MAGENTA
# Use this as an href when the real link is unknown. Never guess a live URL: a wrong link goes to real subscribers.
TODO_URL = 'https://TODO-ADD-LINK'
DEFAULT_FOOTER_REASON = 'Du får denne e-posten fordi du meldte deg på hos Hypopressiv trening Norge.'

# Placeholders found in text drafts -> GHL merge fields. Anything not listed here must be asked about,
# never guessed (see SKILL.md).
PLACEHOLDERS = {
    '[FIRSTNAME]': '{{contact.first_name}}',
    '(FIRSTNAME)': '{{contact.first_name}}',
    '[[contact.first_name]]': '{{contact.first_name}}',   # old Keap spelling of the same field
}

EMOJI_LEAD = re.compile(r'^((?:[\U0001F300-\U0001FAFF☀-➿⭐⏰❤️‍])+)\s*')

# ------------------------------------------------------------------ inline markdown
_ESC = re.compile(r'\\([\\`*_{}\[\]()#+\-.!$%>|~<&:="\'])')   # ':' covers Google Docs' https\\:// exports


def _protect(s):
    return _ESC.sub(lambda m: chr(0xE000 + ord(m.group(1))), s)


def _restore(s):
    return re.sub('[-]', lambda m: chr(ord(m.group(0)) - 0xE000), s)


def convert_placeholders(text):
    for k, v in PLACEHOLDERS.items():
        text = text.replace(k, v).replace(k.replace('[', '\\[').replace(']', '\\]'), v)
    return text


def inline(md, link_style=LINK, strip_links=False):
    s = html.escape(_protect(convert_placeholders(md)), quote=False)

    def link(m):
        return m.group(1) if strip_links else '<a href="%s" target="_blank" style="%s">%s</a>' % (m.group(2), link_style, m.group(1))
    s = re.sub(r'\[([^\[\]]+?)\]\((https?://[^)\s]+|\{\{[^)\s]+)\)', link, s, flags=re.S)
    s = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', s, flags=re.S)
    s = re.sub(r'(?<![\w*])\*(?!\s)(.+?)(?<!\s)\*(?![\w*])', r'<em>\1</em>', s, flags=re.S)
    s = re.sub(r'[ \t]*\n[ \t]*', '<br>', s.strip())
    return _restore(re.sub(r' {2,}', ' ', s))


def clean(md):
    return re.sub(r'^\s*#{1,6}\s*', '', md).strip()


def urls(md):
    return re.findall(r'\]\((https?://[^)\s]+)\)', _protect(md))


# ------------------------------------------------------------------ components
def p(md, style=''):
    """Normal paragraph (.bp, justified like Sadie's examples)."""
    return '<p class="bp"%s>%s</p>\n' % (' style="%s"' % style if style else '', inline(clean(md)))


def greeting(md):
    return p(md)


def hl(inner):
    """Lavender highlight box (.hl) around ready-made inner HTML."""
    return '<div class="hl">\n%s</div>\n' % inner


def box(md):
    return hl('<p class="bp" style="text-align:left;">%s</p>\n' % inline(clean(md)))


def cta(label_md, url=None):
    """Pill button inside a highlight box. Label is plain text (emoji ok). url=None -> TODO_URL placeholder."""
    url = url or TODO_URL
    label = re.sub(r'</?strong>', '', inline(label_md, strip_links=True))
    return hl('<p class="cta"><a class="btn" href="%s">%s</a></p>\n' % (url, label))


def _row(marker, body_html):
    return ('<p class="bp" style="text-align:left;padding-left:30px;text-indent:-30px;">'
            '<span style="display:inline-block;width:30px;text-indent:0;">%s</span>%s</p>\n' % (marker, body_html))


def callout(lines):
    """Highlight box with emoji/bullet rows. `lines`: md strings. A line starting with an emoji becomes a row
    with that emoji as marker, '* ' or '- ' becomes a bullet, anything else becomes a bold title line."""
    out = ''
    for l in [x.strip() for x in lines if x.strip()]:
        m_b = re.match(r'^(?:\*|\\-|-)\s+(.*)$', l)
        if m_b:
            out += _row('&bull;', inline(m_b.group(1)))
            continue
        core = re.sub(r'^\**', '', l)
        m = EMOJI_LEAD.match(core)
        if m:
            out += _row(m.group(1), inline(l[:len(l) - len(core)] + core[m.end():]))
        else:
            out += '<p class="bp" style="text-align:left;"><b>%s</b></p>\n' % inline(l)
    return hl(out)


def features(blocks):
    """Feature list in one box. Each block = title line (emoji optional) + description lines."""
    out = ''
    for i, b in enumerate(blocks):
        lines = [l for l in clean(b).split('\n') if l.strip()]
        title = lines[0].replace('*', '').strip()
        m = EMOJI_LEAD.match(title)
        mk, title = (m.group(1), title[m.end():]) if m else ('', title)
        last = i == len(blocks) - 1
        out += ('<p class="bp" style="text-align:left;margin-bottom:4px;"><span style="display:inline-block;width:30px;">%s</span>'
                '<b style="color:%s;">%s</b></p>\n' % (mk, PURPLE, html.escape(title, quote=False)))
        out += '<p class="bp" style="text-align:left;padding-left:30px;%s">%s</p>\n' % (
            '' if last else 'margin-bottom:20px;', inline('\n'.join(lines[1:])))
    return hl(out)


def sections(groups):
    """Titled bullet groups in one box. `groups`: list of (title_md, [bullet_md, ...])."""
    out = ''
    for gi, (title, bullets) in enumerate(groups):
        t = title.replace('*', '').strip()
        m = EMOJI_LEAD.match(t)
        mk, t = (m.group(1), t[m.end():]) if m else ('', t)
        out += ('<p class="bp" style="text-align:left;margin-bottom:6px;"><span style="display:inline-block;width:30px;">%s</span>'
                '<b style="color:%s;">%s</b></p>\n' % (mk, PURPLE, html.escape(t, quote=False)))
        if bullets:
            lis = ''.join('<li style="margin:0 0 5px;">%s</li>' % inline(x) for x in bullets)
            out += ('<ul style="margin:0 0 %s;padding-left:32px;font-size:15px;line-height:1.6;color:#2f2f2f;text-align:left;">%s</ul>\n'
                    % ('0' if gi == len(groups) - 1 else '20px', lis))
    return hl(out)


def card(name, quotes):
    """Testimonial: name in magenta, quotes in italics, inside a highlight box."""
    out = '<p class="bp" style="text-align:left;"><b style="color:%s;">%s</b></p>\n' % (MAGENTA, inline(name))
    for q in quotes:
        out += '<p class="bp" style="text-align:left;"><i>%s</i></p>\n' % inline(q)
    return hl(out)


def pull(md):
    """Centered Playfair pull quote."""
    return ('<p class="bp" style="font-family:\'Playfair Display\',Georgia,serif;font-style:italic;font-weight:600;color:%s;'
            'font-size:20px;line-height:1.5;text-align:center;margin:26px 0;">%s</p>\n'
            % (PURPLE, inline(clean(md), 'color:%s;text-decoration:underline;' % PURPLE)))


def banner(md):
    """Solid purple urgency bar."""
    return ('<p class="bp" style="background:%s;color:#ffffff;font-weight:700;text-align:center;border-radius:10px;'
            'padding:15px 20px;margin:26px 0;">%s</p>\n' % (PURPLE, inline(clean(md), 'color:#ffffff;text-decoration:underline;')))


def heading(md):
    return '<h2>%s</h2>\n' % inline(re.sub(r'^\*\*|\*\*$', '', clean(md)))


def image(src, alt, first=False, width=None):
    """Image at natural size (never stretched), centered. `src` may be a local placeholder (images/x.png)
    until GHL URLs arrive. Use first=False for stacked follow-up images (small gap)."""
    w = ' width="%d"' % width if width else ''
    return ('<p style="margin:%s;text-align:center;"><img src="%s"%s alt="%s" style="display:block;width:auto;max-width:100%%;'
            'height:auto;margin:0 auto;border-radius:8px;"></p>\n' % ('26px 0 12px' if first else '0 0 12px', src, w, html.escape(alt, quote=True)))


def countdown(snippet=None):
    """GHL countdown timer. Pass the exact snippet from the timer's Copy Code; without it a visible-in-source
    placeholder comment is left so the gap can't be forgotten."""
    if not snippet:
        return '<!-- COUNTDOWN TIMER: paste the GHL timer snippet (Marketing > Countdown Timers > Copy Code) here -->\n'
    snippet = snippet.strip()
    if 'max-width' not in snippet:
        snippet = snippet.replace('style="display: block;', 'style="display: block; max-width:100%; height:auto;', 1)
    return '<div style="margin:26px 0;text-align:center;">%s</div>\n' % snippet


def signature(lines):
    """Sign-off lines from the copy (e.g. 'Hjertelig hilsen ❤️', 'Sadie'). The footer already shows Sadie's
    photo, so keep this as plain text exactly as written."""
    return '<p class="bp" style="text-align:left;margin-top:26px;">%s</p>\n' % '<br>'.join(inline(l) for l in lines)


# ------------------------------------------------------------------ assembly
def assemble(body_html, subject='', preheader='', label='', footer_reason=None):
    meta = ''
    if subject or preheader or label:
        meta = '\n<!-- %s\nSubject: %s\nPre-header: %s\n-->' % (label, subject.replace('--', '- -'), preheader.replace('--', '- -'))
    with open(TEMPLATE, encoding='utf-8') as f:
        t = f.read()
    return (t.replace('@@META@@', meta)
             .replace('@@FOOTER_REASON@@', footer_reason or DEFAULT_FOOTER_REASON)
             .replace('@@BODY@@', body_html))


def write(path, doc):
    os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(doc)
    return path
