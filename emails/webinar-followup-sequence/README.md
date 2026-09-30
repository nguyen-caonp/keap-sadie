# Webinar follow-up sequence (Feb 2026)

Redesign of the 11 post-webinar emails from `Auto Webinar Funnel emails - Feb 2026`, using the same
shell and palette as `emails/webinar-reminder-sequence` (branch `claude/email-html-design-1pdtb3`).

The copy is taken word-for-word from the source doc. Every `[[contact...]]` merge field and every
link is unchanged (checked programmatically against the source). Subject line and pre-header sit in
the HTML comment at the top of each file. Keap does not read that comment, so you set them in the
email settings.

| File | Send time | Subject |
|---|---|---|
| email-01-for-en-kveld | Right after | For en kveld! |
| email-02-reprise | Thu morning | "Få med deg hemmelighetene …" |
| email-03-kristin | Thu afternoon | "Ikke f%$n skal jeg bli en sånn dame …" |
| email-04-for-godt-til-aa-vaere-sant | Fri | Dette virker for godt til å være sant |
| email-05-tankeeksperiment | Sat morning | Gjør dette tankeeksperimentet |
| email-06-nederst-paa-lista | Sat evening | Slutt å sette deg selv nederst på lista |
| email-07-angre | Sun morning | Det eneste du vil angre på er at du ikke startet før |
| email-08a-bente | Sun lunch | Hils på Bente |
| email-08b-raske-resultater | Sun afternoon | Hvor raske resultater vil du ha |
| email-09-forste-steget | Sun evening | Du trenger bare å ta det første steget |
| email-10-dorene-lukkes | Sun night | Dørene lukkes NÅ |

(The source doc has two "Email 8"s, so they are named 8a / 8b here.)

## Manual steps

1. **Host the images.** The source embeds screenshots as base64, which Keap and Gmail strip. They are
   extracted to `images/` (9 files). Upload them to Keap's image library (or any host), then
   find-and-replace `src="images/` with `src="https://<your-host>/` in the HTML.
2. **Paste each file** into a Keap HTML / custom-code email. Set subject and pre-header from the
   comment at the top.
3. **Send yourself a test** and check `[[…]]` values render (they only merge inside Keap; a browser
   preview shows them raw). Check especially how `[[…Offerdeadline]]` reads in the sentences below.
4. **Check the footer opt-out link.** It is copied from the reminder sequence and contains one
   specific `inf_contact_key`. Make sure Keap swaps it per recipient (or replace it with Keap's own
   opt-out merge).

## Limitations

- Fonts (Questrial, Playfair Display) fall back to Arial / Georgia in Gmail and Outlook, as in the reminder sequence.
- Outlook desktop ignores rounded corners and the gradient bars. Buttons still work but are square.
- Buttons are whole-block links.
- No dark-mode styling.
- All files are 11–22 KB, well under Gmail's ~102 KB clipping limit.

## Changes beyond restyling (please confirm)

- Email 8a: the "[[contact.first_name]], dette er Bente 💗" greeting was baked into the photo, so it would never merge. I cropped it off the image and made it live text.
- Emails 4 and 6: the "reprise" lines in the source are bracketed text with no link. I linked them to `https://webinar.hypopressivtrening.no/reprise`.
- "Tusen takk Sadie" screenshot appears in emails 4, 5 and 7 (three slightly different crops in the source, one with a "Content" badge). All three now use one clean image.
- Added the standard disclaimer ("Resultater varierer …") and the reminder-sequence footer.
- Image order in email 4 follows the source doc; the screenshots do not obviously belong to the testimonial next to them.

## Agreed copy edits (applied on top of the source doc)

- Email 10: "2025" changed to "2026" (no 2024 or 2025 remains).
- Women helped is always "12.000+": email 4 "snart 10.000" and "over 12.000", and email 7 "over 12.000+", were changed.
- Email 7: the whole top CTA sentence (🔗🔗 and the text) now links to `/blimed`.
- Hard-coded details ("mandag kl 18.00", "søndag kl 24:00", prices, "reprise kl 20:30") are kept as in the source. Update them for the next launch.
- Member photos and screenshots are cleared for reuse.

## Copy issues left as-is (not changed, your call)

- Email 8b: "1450k" (should be kr), "kun599/mnd", "inkluder**t**", "en **krop**"; emails 6 and 8a: "inkluder**et**".
- Training pack value: 743 kr (email 1) vs 793 kr (email 8b). Discount: "250kr" (1) vs "25%" (later).
- "innen **søndag** [[Offerdeadline]]" (emails 2, 3, 4): reads "søndag søndag …" if the field already contains the weekday.
- Age range differs: "6-87" (email 7), "18 og 87" (8a), "18-85" (4).
