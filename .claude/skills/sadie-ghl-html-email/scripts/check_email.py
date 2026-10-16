#!/usr/bin/env python3
"""QA for Sadie's GHL HTML emails.

    python3 check_email.py email.html [more.html ...] [--source draft.txt]

Exit code 1 if any FAIL. WARN lines are things to report to the user (missing images, timers, Keap tokens).
With --source (the original text draft) it also checks that every merge field and every link from the draft
made it into the HTML unchanged.
"""
import re
import sys
import collections

sys.path.insert(0, __file__.rsplit('/', 1)[0])
from ghl_email import convert_placeholders  # noqa: E402

FOOTER_MARK = '<div class="ftr">'


def split_doc(doc):
    head, _, rest = doc.partition('<div class="emb">')
    body, _, footer = rest.partition(FOOTER_MARK)
    return head, body, footer


def tokens(text):
    return collections.Counter(re.findall(r'\{\{[^}]+\}\}', text))


def check(path, source=None):
    res = []  # (level, message)
    doc = open(path, encoding='utf-8').read()
    head, body, footer = split_doc(doc)
    body_nc = re.sub(r'<!--.*?-->', '', body, flags=re.S)   # body without comments

    if not doc.lstrip().lower().startswith('<!doctype html>'):
        res.append(('FAIL', 'does not start with <!doctype html> (Sadie\'s GHL emails are full documents)'))
    for need, why in [('class="topbar"', 'purple logo bar'), ('class="emb"', 'content wrapper'), ('class="ftr"', 'footer with Sadie bio'),
                      ('{{email.unsubscribe_link}}', 'GHL unsubscribe merge field')]:
        if need not in doc:
            res.append(('FAIL', 'missing %s (%s)' % (need, why)))

    if re.search(r'\[\[[^\]]+\]\]', doc):
        found = sorted(set(re.findall(r'\[\[[^\]]+\]\]', doc)))
        res.append(('WARN', 'Keap-style [[...]] tokens left (ask the user for the GHL field): %s' % ', '.join(found)))
    if 'infusionsoft' in doc.lower():
        res.append(('FAIL', 'Keap/Infusionsoft link present - Sadie only uses GHL now'))
    if re.search(r'\*\*|\\[!\-+_.\[\]]', body_nc):
        res.append(('FAIL', 'leftover markdown/backslash escapes in body'))
    if re.search(r'FIRSTNAME|\(COUNTDOWN\)', body_nc):
        res.append(('FAIL', 'unconverted placeholder in body (FIRSTNAME / (COUNTDOWN))'))
    if 'TODO' in doc:
        res.append(('WARN', 'TODO marker left in file'))

    imgs = re.findall(r'<img [^>]*src="([^"]+)"', body_nc)
    local = [i for i in imgs if not i.startswith('http')]
    if any(i.startswith('data:') for i in imgs):
        res.append(('FAIL', 'base64 image in body (GHL/Gmail strip these)'))
    if local:
        res.append(('WARN', 'images still local, need GHL-hosted URLs from the user: %s' % ', '.join(local)))
    if '<!-- COUNTDOWN TIMER' in body:
        res.append(('WARN', 'countdown timer slot is empty - needs the GHL timer snippet'))

    first_p = re.search(r'<p class="bp"[^>]*>(.*?)</p>', body, flags=re.S)
    if first_p and '{{contact.first_name}}' not in first_p.group(1):
        res.append(('WARN', 'first paragraph has no {{contact.first_name}} greeting'))

    links = re.findall(r'href="([^"]+)"', body_nc)
    for l in links:
        if not (l.startswith('http') or l.startswith('{{')):
            res.append(('FAIL', 'suspicious href: %s' % l))
    if len(doc.encode('utf-8')) > 100 * 1024:
        res.append(('FAIL', 'over 100 KB: Gmail will clip it'))

    if source:
        src = convert_placeholders(open(source, encoding='utf-8').read())
        want = tokens(src)
        have = tokens(body_nc)
        have.pop('{{contact.id}}', None)  # lives in the countdown snippet's tracking link
        if want != have:
            res.append(('FAIL', 'merge fields differ from draft. draft=%s html=%s' % (dict(want), dict(have))))
        src_urls = set(re.findall(r'\]\((https?://[^)\s]+)\)', src)) | set(re.findall(r'(?<![\]\(])https?://[^\s)<>]+', src))
        missing = sorted(u for u in src_urls if u not in set(links))
        if missing:
            res.append(('FAIL', 'links from the draft missing in HTML: %s' % ', '.join(missing)))

    res.append(('INFO', 'merge fields: %s | links: %s | images: %d | %d KB' % (
        dict(tokens(body_nc)) or 'none', sorted(set(links)) or 'none', len(imgs), len(doc.encode('utf-8')) // 1024)))
    return res


def main(argv):
    src = None
    if '--source' in argv:
        i = argv.index('--source')
        src = argv[i + 1]
        argv = argv[:i] + argv[i + 2:]
    failed = False
    for f in argv:
        print('==', f)
        for level, msg in check(f, src):
            print('  %-4s %s' % (level, msg))
            failed |= level == 'FAIL'
    return 1 if failed else 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
