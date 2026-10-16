---
name: sadie-ghl-html-email
description: Turn text emails for Sadie Lawler / Hypopressiv Trening Norge into finished, paste-ready GoHighLevel (GHL) HTML emails in her brand template. Use this whenever the user pastes, uploads or @-mentions an email draft or a whole email sequence for Sadie (Norwegian copy, "Emne:", "Subject line:", "Pre-header", "Preview", "Hei [FIRSTNAME]", "E-post 1", webinar reminders, follow-ups, HYPO GOLD or course sales emails), even if they never say "HTML". Also use it to edit, extend or fix Sadie's existing HTML emails (images, links, countdown timer, greetings, typos). Sadie sends only through GoHighLevel now, never Keap, so output GHL merge fields like {{contact.first_name}}, never Keap [[...]] syntax.
---

# Sadie GHL HTML email

Sadie's emails are written as plain text first. Your job is to turn each draft into a complete HTML email that
looks exactly like her existing GHL emails and can be pasted straight into a GHL custom-code email. The user
should not have to ask for HTML: a pasted text email for Sadie *is* the request.

**GHL only.** Sadie used Keap before and no longer does. Old emails in this repo (`emails/webinar-*-sequence`)
are Keap-era (inline-styled fragments, `[[...]]` fields, Infusionsoft opt-out link). Do not copy that style or
those fields into new work. If the user ever says an email goes through Keap, confirm before changing the approach.

## Workflow

1. **Read the whole draft first.** Note: subject, pre-header, send timing, audience, every link, every merge
   field or placeholder, every image or "(COUNTDOWN)" style note, and any sales-page outline mixed in. A document
   may contain non-email material (e.g. a landing-page proposal). Convert only the emails and say what you skipped.
2. **Build each email** from `assets/ghl-email-template.html` using `scripts/ghl_email.py` (see "Building").
   Keep copy word for word. Choose components by the job each part of the email does (see `references/components.md`).
3. **Run the checker** `python3 scripts/check_email.py <files> [--source draft.txt]` and fix every FAIL.
4. **Look at it.** Render a desktop and a phone screenshot if Chromium/Playwright is available
   (`scripts/preview.py`) and fix anything cramped or broken. GHL-hosted logo/avatar won't load in a sandbox;
   that is expected.
5. **Report back** with the open-items list below. The user explicitly wants to be told what is missing so they
   can supply it, so put that list up front rather than burying it.
6. **Save and push** to the branch the session names (usually under `emails/<sequence-name>/`, one file per
   email plus a short README with subjects, pre-headers, send times and open items). Commit and push; open a PR
   only if asked.

## Hard rules (and why)

- **Never reword the copy.** Sadie's voice is deliberate (capital letters for emphasis, "❤️", "😱"). Typos,
  inconsistencies and odd phrasing get *flagged* in a short list, not silently fixed; the user decides. Apply only
  edits the user has explicitly agreed (a few standing decisions are in `references/brand-and-rules.md`).
- **Merge fields: preserve exactly, never invent.** `[FIRSTNAME]`, `(FIRSTNAME)` → `{{contact.first_name}}`
  (the only mapping you may make yourself). Any other field must be used exactly as the user supplied it. If a
  draft contains a Keap field like `[[contact.custom_fields.Offerdeadline]]`, keep it as written, flag it as
  Keap syntax and ask for the GHL field. A wrong guessed field sends "{{contact.something}}" to real subscribers.
- **Links: keep every URL.** If button or link text has no URL in the draft, ask for it. Only reuse a link
  from the user's *own other emails in the same job* when it is unmistakably the same offer (for example every
  email in a HYPO GOLD sequence points to the same registration page), and say you did. When you can't tell,
  do **not** guess a real-looking URL (a wrong page would be sent to real subscribers, and "I flagged it" is easy
  to miss). Put `TODO_URL` (`https://TODO-ADD-LINK`) as the href: `cta(label)` does this by default and the
  checker warns about it. Known links are in `references/brand-and-rules.md`.
- **Every email greets by first name.** If the draft has no greeting, add one in Sadie's own style
  (`Hei {{contact.first_name}},`, `Hei fineste …!`, `Hei …`, `God morgen …!`, `Hei kjære …,`, `Hei igjen …,`),
  vary them across a sequence, and tell the user you added them.
- **Images:** never base64. Drafts exported from Google Docs embed images; extract them, show/describe them to
  yourself, save them next to the emails in `images/` and reference `images/<name>` as a placeholder until the user
  uploads to GHL media and sends back `https://assets.cdn.filesafe.space/...` URLs. Then swap the URLs in place.
  Show images at natural size (never stretch). If the user splits one screenshot into pieces, stack them with no gap.
  Check images for baked-in merge fields or placeholder text (e.g. "[[first_name]]" typed into the picture): crop
  it out and make it live text.
- **Hard-coded details stay** (dates, weekdays, prices, "mandag kl 18.00", "kun gyldig i 4 dager"). Prices that
  differ between emails may be intentional. Flag only genuine contradictions and ask.
- **Number of women helped is 12.000+** in body copy: write "12.000+ kvinner", or just "mer enn 12.000" / "over 12.000"
  when a "more than" is already there (never both). The footer bio keeps Sadie's "12 000".

## Building

```python
import sys; sys.path.insert(0, '.claude/skills/sadie-ghl-html-email/scripts')
from ghl_email import *
body = (greeting('Hei {{contact.first_name}},') + p('Text with **bold**.') +
        callout(['**Du kan velge:**', '💪 **6 måneder for kun 2500,-**']) +
        cta('JA, JEG VIL BLI MED', 'https://registration.hypopressivtrening.no/hypo-gold') +
        signature(['Hjertelig hilsen ❤️', 'Sadie']))
write('emails/my-sequence/email-01-slug.html',
      assemble(body, subject='...', preheader='...', label='E-POST 1 — DAG 1'))
```

Write the build script in the scratchpad/temp directory, not the repo. When drafts are long, parse the text into
paragraph blocks programmatically instead of retyping, so copy and merge fields can't drift. Subject and
pre-header go into the HTML comment in `<head>` (GHL's subject/preview fields are set in the GHL UI, tell the user).

## Footer and the template

Use the template unchanged: purple logo bar, content in `.emb`, footer with Sadie's photo, bio and the GHL
unsubscribe merge field. The footer line "Du får denne e-posten fordi du meldte deg på hos Hypopressiv trening Norge."
suits webinar sign-ups. For other audiences (e.g. past course buyers who are not HYPO GOLD members) it may not be
true; ask the user once for their standard wording and pass it as `footer_reason` to `assemble`. Do not add the
old Keap "Resultater varierer…" disclaimer: it is not in Sadie's GHL template.

## Countdown timers

GHL has built-in timers (Marketing → Countdown Timers). For a campaign where everyone shares the same deadline
use a *fixed* timer; per-contact (dynamic) timers start when the email is opened and can mislead. Custom-HTML emails
need the timer's **Copy Code** snippet: leave `countdown()` (placeholder comment) until the user pastes it, then
insert it verbatim (the helper only adds `max-width:100%` so it can't overflow on phones). Put it right above the
main button, or where the draft says "(COUNTDOWN)". A timer can't be edited after it has been sent, so tell the
user to send a test first. Norwegian labels: Dager / Timer / Minutter / Sekunder; brand purple #5C3884.

## Open-items report (always give this)

After building, list in plain language, grouped:
1. **Needed from the user:** missing links, GHL image URLs, countdown snippet, unknown merge fields, audience footer wording.
2. **Assumptions you made:** links filled in, greetings added, placeholders converted, stale years, images cropped.
3. **Copy issues left as-is:** typos and contradictions, with the exact phrase.
4. **Table of subject, pre-header and suggested send time** (Norway time, Europe/Oslo) for sequences: mornings ~08:00-09:00,
   afternoon ~14:00-15:00, evening ~18:00-20:30, the last email 3-4 hours before a deadline, never two emails closer
   than about 5-6 hours unless the draft demands it.

## Finish

Say clearly what you verified (checker passed, screenshots looked right) and what you could not (GHL-hosted images
and timers can't load in a sandbox, merge fields only fill in inside GHL). Don't claim a link or image works if you
couldn't open it.
