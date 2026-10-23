# Components

Pick components by the job a part of the email does. The helper functions in `scripts/ghl_email.py` produce
exactly these. All of them use only the classes in the template's `<style>` block plus small inline styles, so
they survive GHL and Gmail. Don't add new CSS classes; add inline styles instead.

| Job in the copy | Component | Notes |
|---|---|---|
| Normal paragraph | `p()` → `<p class="bp">` | justified text like Sadie's own emails; use `style="text-align:left;"` for short lines |
| Greeting | `greeting()` / first `p()` | always the first paragraph; contains `{{contact.first_name}}` |
| One strong standalone statement ("Det er at ALLE KVINNER FORTJENER…") | `pull()` | Playfair italic, centered, purple |
| Deadline / urgency line ("Dette tilbudet er kun gyldig i 4 dager", "Om noen timer stenger…") | `banner()` | solid purple bar, white text |
| Offer options, "Du kan velge:", bonus lists, 💪/🎉/👉🏼 rows | `callout()` | lavender box; emoji becomes a hanging marker; plain lines become bold titles |
| Benefit list with a title and a description each | `features()` | emoji + purple title + description |
| Titled groups of bullets ("Live-sendinger hver mandag:" + bullets) | `sections()` | one box, several groups |
| Testimonial with a name | `card(name, quotes)` | magenta name, italic quotes |
| Emphasised aside, guarantee, bold question | `box()` | lavender box, left aligned |
| Section heading inside a long email (objections, "BONUS #1") | `heading()` | Playfair italic `<h2>` (the `.emb h2` rule is an addition to Sadie's template) |
| Main call to action | `cta(label, url)` | pill button in a lavender box; label is short (≤ ~60 chars) |
| Link inside a sentence | inline `[text](url)` | magenta, underlined |
| Screenshot / photo | `image(src, alt)` | natural size, centered, rounded; stack several with `first=False` |
| Countdown timer | `countdown(snippet)` | right above the main button, or where the draft says (COUNTDOWN) |
| Sign-off from the copy | `signature(lines)` | plain text; the footer already carries Sadie's photo and name |

One main CTA per email is normal. Long sales emails repeat the same button once or twice (after the offer,
and at the end). Don't invent extra buttons or button labels: if the draft has only an inline link, keep an
inline link and offer a button in the report.

## Webinar reminder pattern (from Sadie's own GHL email)

Reminders about a live webinar use two lavender boxes: calendar buttons, then the join button. This is the
reference markup (merge fields exactly as Sadie uses them):

```html
<p class="bp">Legg til sendingen i kalenderen din (<a href="https://calendar.google.com/calendar/render?action=TEMPLATE&text=Webinar:+Sannheten+om+kjernen+og+bekkenbunnen&dates={{contact.webinar_calendar_dates}}&details=Din+personlige+lenke+til+sendingen:+{{contact.webinar_join_url}}&location={{contact.webinar_join_url}}" style="color:#2636C8">trykk her</a>) nå så du husker å bli med:</p>
<div class="hl"><p class="cta"><a class="btn" href="(same calendar URL)">Legg til i kalenderen</a></p>
<p class="bp" style="font-size:13px;line-height:1.5;margin-top:4px">Bruker du Outlook eller Apple-kalender? <a href="{{contact.webinar_calendar_url}}">Last ned kalenderfilen her</a>.</p></div>
<div class="hl"><p class="cta"><a class="btn" href="{{contact.webinar_join_url}}">🔗🔗Bli med {{contact.webinar_date_text}} kl {{contact.webinar_time_text}} med denne linken🔗🔗</a></p></div>
<p class="bp">Sees på {{contact.webinar_weekday}}, Sadie ❤️</p>
```

Weekday/date/time copy in reminders uses `{{contact.webinar_weekday}}`, `{{contact.webinar_date_text}}`,
`{{contact.webinar_time_text}}`; the join link is `{{contact.webinar_join_url}}`. Only reuse these in reminders
when the draft clearly has the same slots; otherwise ask which field the user wants.

## Email-client reality

GHL, Gmail and Apple Mail render this fine. Outlook desktop ignores rounded corners. Gmail clips emails over
~102 KB (Sadie's are 4-22 KB). Web fonts fall back to Arial/Georgia. Merge fields only fill in inside GHL.
