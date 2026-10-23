# Sadie: brand, links, fields and standing decisions

Read this when building or editing emails. Facts here come from Sadie's own GHL emails and from decisions the
user made while building the first sequences (Oct 2026). If the user changes a rule, follow the user.

## Brand

| Color | Code | Used for |
|---|---|---|
| Purple (main) | `#5C3884` | logo bar, buttons, headings, countdown timer |
| Magenta | `#963885` | links, testimonial names |
| Lilac | `#D9B2D4` | borders, footer top line |
| Lavender | `#EDE8F4` | highlight boxes (`.hl`) |
| Cream | `#F0F0E8` | footer background |

Fonts: Arial body, Playfair Display italic for headings, pull quotes and the footer signature.
Norwegian (bokmål) throughout. Sadie writes warm and first person, short paragraphs, emoji sparingly but
deliberately (🎉 💪 😱 👉🏼 ❤️), CAPITALS for emphasis.

## GHL merge fields known to exist (from Sadie's webinar reminder email)

`{{contact.first_name}}`, `{{contact.webinar_weekday}}`, `{{contact.webinar_date_text}}`,
`{{contact.webinar_time_text}}`, `{{contact.webinar_join_url}}`, `{{contact.webinar_calendar_dates}}`,
`{{contact.webinar_calendar_url}}`, `{{email.unsubscribe_link}}` (footer, required),
`{{contact.id}}` (only inside a countdown timer's tracking link), `{{right_now.date_time_iso}}` (dynamic timers).

Use a field only when the user supplied it or it is in this list *and* the draft clearly means it. Old Keap fields
(`[[contact.custom_fields.NOWebinarDate]]`, `Offerdeadline`, `Fellesoppstart`, `WFJoinLink`, `MeetingsCID`, …)
have no confirmed GHL equivalent: keep as written, flag, ask. Only `first_name` maps automatically.

## Links seen in Sadie's campaigns (per campaign, never swap one for another silently)

| Purpose | URL |
|---|---|
| HYPO GOLD registration (past course buyers sequence) | `https://registration.hypopressivtrening.no/hypo-gold` |
| Main course sales page | `https://kurs.hypopressivtrening.no` (`/blimed` is a variant used once) |
| Webinar replay | `https://webinar.hypopressivtrening.no/reprise` |
| Podcast episode page | `https://webinar.hypopressivtrening.no/podcast` |
| HYPO GOLD LIVE join page on Kajabi (course platform, not email) | `https://hypopressiv-trening-norge.mykajabi.com/products/grunnkurs-hypopressiv-trening-hypogold/categories/2154620135/posts/2174635267` |
| Instagram DM (Q&A) | `https://ig.me/m/hypopressivtreningnorge` |

## Standing decisions (user-approved)

- Women helped: always **12.000+** in body copy (drafts sometimes say 10.000 / 11.000 / "over 12.000"). After "mer enn" / "over" write plain 12.000.
- Years: drafts sometimes carry an old year (2024/2025). The user approved updating to **2026** once; for later
  campaigns propose the current campaign year and say you changed it.
- Prices, dates, weekdays, times and "kun gyldig i N dager" are hard-coded in the copy on purpose. Don't touch.
  Different values for the same thing across emails (e.g. a training pack valued at 743 kr vs 793 kr) can be
  intentional; mention it once, don't change it.
- Age ranges ("18-87") should agree between emails of one sequence; a joke like "6-87 … ok, kanskje ikke
  6-åringene" is intentional.
- Typos the user approved fixing in past sequences were obvious spelling slips ("inkluderet" → "inkludert",
  "tilbydd" → "tilbudt", "for få" → "for å få", "kun599" → "kun 599"). Still list them and get a yes first, unless the user
  has said "fix typos" for this job. Never touch quoted testimonials (their spelling is theirs).
- Button brackets in drafts (`[JA, JEG TRENGER…]`) are placeholders: drop the brackets.
- Testimonial images/screenshots and member photos are cleared for reuse (the user confirmed).
- Drafts may mark italics with `\_word\_` (escaped underscores): treat as italic.

## Audience notes

- HYPO GOLD *member* reminders (Friday "på mandag kl. 19" and Monday "i dag kl. 19" emails): current members. Same boilerplate at the end of each
  (Kajabi join link, "Husk at HYPO GOLD er et variert tilbud…", new Monday recordings, a Zoom NB note ending "Hjertelig hilsen, Sadie & teamet ❤️").
  Build the Zoom NB as a `box()` and the sign-off as `signature()`; save under `emails/hypogold-member-reminders/`.

- Webinar sequences (reminders before, follow-ups after): audience signed up for the webinar.
- HYPO GOLD "come back" sequence: people who bought the main course but have no active HYPO GOLD membership.
- If you don't know the audience, ask before choosing the footer reason (see SKILL.md).

## Send-time conventions (Norway time)

Day-based sequences: morning 08:00-09:00, midday/afternoon 14:00-15:00, evening 18:00-20:30. Deadline day:
first email early (08:00), last email 3-4 hours before the close ("Om noen timer…"). Podcast-style evening
content ~17:00. Always state the timezone (Europe/Oslo).
