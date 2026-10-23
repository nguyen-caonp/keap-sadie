# HYPO GOLD sales sequence for previous course participants (GoHighLevel)

8 emails from `Sales sequence for previous course participants to resell people to HypoGold`,
built on the same GoHighLevel template as your example email (purple logo bar, lavender highlight boxes,
pill buttons, footer with Sadie's photo and bio). Each file is a complete HTML document: paste it into a
GHL custom-code / HTML email. Subject and pre-header are in the HTML comment in `<head>` (set them in GHL).
The "Forslag på ny salgside" section at the end of the doc is a sales-page outline, not an email, and is not included.

| File | When | Subject |
|---|---|---|
| email-01-give-it-another-try | Day 1 | Du får kun tilgang til dette fordi du har hatt kurset mitt før |
| email-02-verdi-fokus | Day 2 morning | Dette får du {{contact.first_name}} |
| email-03-innvendinger | Day 2 afternoon | "Jeg rakk aldri å bruke det" (og andre innvendinger) |
| email-04-hva-skjer-i-hypogold | Day 3 morning | Her er hva du går glipp av hver måned {{contact.first_name}} |
| email-05-testimonials | Day 3 afternoon/evening | "HYPO GOLD hjelper meg å holde motivasjonen oppe" |
| email-06-kristins-historie | Day 4 morning | "Jeg holdt på å gi opp" - Kristins historie |
| email-07-oppsummering-faq | Day 4 afternoon | Vil ha deg i mål {{contact.first_name}}! |
| email-08-siste-sjanse | Day 4 evening | Siste sjanse, {{contact.first_name}} |

## Merge fields

Only two are used, written as in your GHL example: `{{contact.first_name}}` (greeting and body) and
`{{email.unsubscribe_link}}` (footer). Logo, Sadie's photo, bio and footer text are copied from the example unchanged.
The old Keap opt-out link is not used here. A browser preview shows `{{ }}` raw; they merge inside GHL.

## Countdown timer

Emails 4, 6, 7 and 8 contain your GHL fixed countdown timer snippet (email 4 at the spot marked "(COUNTDOWN)" in the source; in 6, 7 and 8 just above the main button). The snippet is unchanged except that I added `max-width:100%; height:auto;` to the image so it can't overflow on phones. It contains the extra merge field `{{contact.id}}` (in the timer's tracking link) and has an empty `uniqueId=`, which is as GHL generated it. A timer can only be edited before it goes out in a sent email, so send yourself a test first and check the end time.

## Still needed

None. Email 5 images and the countdown timer are in. Remaining details from you will go here.

## Assumptions (please confirm)

- **One link everywhere.** The only URL in the doc is `https://registration.hypopressivtrening.no/hypo-gold` (emails 1-3). Emails 4-8 had link text but no URL, so I used the same link (email 4 inline; email 5 "Sjekk det ut her!" and the button; buttons in 6, 7, 8).
- `[FIRSTNAME]` and `(FIRSTNAME)` are written as `{{contact.first_name}}` (parentheses dropped).
- "11.000" is now "12.000+" (emails 1 and 7).
- Square brackets around button labels in the doc were placeholders and are removed.
- `_hvorfor_` in email 3 is shown in italics. Email 4 has only the inline link, no button, as in the source.
- The webinar reminder disclaimer ("Resultater varierer...") is not in your GHL example, so it is not included here.
- The footer line "Du får denne e-posten fordi du meldte deg på hos..." is from your example. Email 1 says the reader bought the course, so you may want different wording for this audience.

## Copy issues left as-is (your call)

- Email 3: "med fullt støtte" (full støtte) and "så der det faktisk ikke slik" (var det).
- Email 2: stray ")" in "både online eller fysisk!). Verdi 1050kr."
- The offer period is hard-coded ("kun gyldig i 4 dager", "ut dagen i morgen", "ved midnatt"), as in the source.
