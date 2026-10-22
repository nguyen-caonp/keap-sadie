# Course onboarding emails (GHL)

| File | Audience | Subject |
|---|---|---|
| privattime-booking-info | People who bought the course with a private session included | not in the draft: set it in GHL |

## privattime-booking-info: open items

- **Needed:** the subject line (the draft has none).
- **Booking link:** "HER på denne siden" points to `https://hypopressivtrening.no/bestill-time` (supplied by you; not opened by me).
- **Merge fields:** only `[[contact.first_name]]` was in the Keap email; it is now `{{contact.first_name}}`. No other fields.
- **Footer** is the default "Du får denne e-posten fordi du meldte deg på hos Hypopressiv trening Norge." Send your standard wording for course buyers if you want it changed.
- **Copy left as written:** space before the "!" in the greeting ("…first_name }} !"); the trainer names and "denne felles oppstarten" are specific to this start (update when reused); "gyldig i 6 måneder" is hard-coded.
