# HYPO GOLD sales sequence for previous course participants

8 emails from `Sales sequence for previous course participants to resell people to HypoGold`,
in the same design as `emails/webinar-followup-sequence`. Subject and pre-header are in the HTML
comment at the top of each file (Keap does not read it, so set them in the email settings).
The "Forslag på ny salgside" section at the end of the doc is a sales-page outline, not an email, and is not included.

| File | When | Subject |
|---|---|---|
| email-01-give-it-another-try | Day 1 | Du får kun tilgang til dette fordi du har hatt kurset mitt før |
| email-02-verdi-fokus | Day 2 morning | Dette får du [[contact.first_name]] |
| email-03-innvendinger | Day 2 afternoon | "Jeg rakk aldri å bruke det" (og andre innvendinger) |
| email-04-hva-skjer-i-hypogold | Day 3 morning | Her er hva du går glipp av hver måned [[contact.first_name]] |
| email-05-testimonials | Day 3 afternoon/evening | "HYPO GOLD hjelper meg å holde motivasjonen oppe" |
| email-06-kristins-historie | Day 4 morning | "Jeg holdt på å gi opp" - Kristins historie |
| email-07-oppsummering-faq | Day 4 afternoon | Vil ha deg i mål [[contact.first_name]]! |
| email-08-siste-sjanse | Day 4 evening | Siste sjanse, [[contact.first_name]] |

## Still needed from you

1. **Countdown timer (email 4).** The source only says "(COUNTDOWN)". The spot is marked with an HTML comment in `email-04-hva-skjer-i-hypogold.html`. Send me the countdown image URL or embed code, or tell me to leave it out.
2. **Keap links for the 3 chat screenshots in email 5.** They are in `images/` (`chat-anne-kari-cathrine-marit.png`, `chat-ann-charlotte.png`, `chat-marit.png`). The HTML still points at `images/...` until you send the hosted URLs.

## Assumptions (please confirm)

- **One link everywhere.** The only URL in the doc is `https://registration.hypopressivtrening.no/hypo-gold` (emails 1, 2 and 3). Emails 4-8 had link text but no URL, so I used that same link: email 4 (inline "HYPO GOLD tilbudet som du finner her"), email 5 ("Sjekk det ut her!" and the button), and the buttons in emails 6, 7 and 8. The 6-month and 1-year options are on the same page ("Betaling skjer på neste side").
- **Merge field.** `[FIRSTNAME]` and `(FIRSTNAME)` are written as `[[contact.first_name]]`, exactly as in the other sequences (the "(FIRSTNAME)" parentheses were dropped).
- **12.000+** replaces "11.000" (emails 1 and 7), following your rule that the number is always 12.000+.
- The square brackets around button labels in the doc (e.g. "[JA, JEG TRENGER...]") were placeholders and are removed.
- In email 3, `_hvorfor_` is shown in italics.
- Email 4 has only the inline link, no button, as in the source. I can add one if you give me the label text.

## Copy issues left as-is (your call)

- Email 3: "med fullt støtte" (full støtte) and "så der det faktisk ikke slik" (var det).
- Email 2: stray ")" in "både online eller fysisk!). Verdi 1050kr."
- The offer period is hard-coded ("kun gyldig i 4 dager", "ut dagen i morgen", "ved midnatt"), as in the source.
