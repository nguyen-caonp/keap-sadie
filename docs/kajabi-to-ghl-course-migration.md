# Kajabi → Go High Level Course Migration Guide

**Site:** Hypopressiv Trening Norge (Kajabi site ID `171481`)
**Scope:** Content-only migration. Kajabi is used purely as a course host here — pricing,
checkout, and payment processing live on a separate platform and are **out of scope**.
This guide only covers moving course structure/content and access-granting logic into GHL.

---

## Courses in scope

| # | Course | Kajabi Product ID | Members | Type |
|---|--------|-------------------|---------|------|
| 1 | Grunnkurs Hypopressiv Trening | `680309` | 9,283 | Flat evergreen |
| 2 | Grunnkurs Hypopressiv Trening + HypoGold | `2148488003` | 1,853 | Drip evergreen (bundle) |
| 3 | Gravidkurs Hypopressiv Trening | `702398` | 52 | Flat evergreen (nested submodules) |

---

## 1. Grunnkurs Hypopressiv Trening (id 680309)

**Kajabi structure:** 16 modules, ~48 lessons, no submodules, no drip — everything unlocks at once.

| Module | Lessons | State |
|---|---|---|
| Start her | 5 | published (1 lesson still draft: "Min historie") |
| Uke 1: Pusteteknikken | 3 | published |
| Uke 2 - 3: Stående og liggende | 2 | published |
| Uke 4 - 5: Stående + på alle 4 | 2 | published |
| Uke 6 - 7: Panna ned + asymmetrisk liggende | 2 | published |
| Uke 8: Teknikk | 2 | published |
| Uke 9: Skredderstilling | 2 | published |
| Uke 10 - 11: Fremoverbøyd | 2 | published |
| Uke 12: Sjekk hvor langt du har kommet | 3 | published |
| Bonusbiblioteket | 11 | published |
| Test (videoene du så før du fikk tilgang) | 3 | published |
| Live spørretimer/sendinger fra facebookgruppen | 4 | published |
| MOTIVASJONSMAI | 2 | **draft — do not migrate unless reactivated** |
| PANGSTART - alle sendinger | 6 | **draft — do not migrate unless reactivated** |

**GHL target:** 1 GHL "Product/Course" → Categories = modules above → Lessons = same order.
No drip rules needed; unlock everything on enrollment.

### Steps
1. Create course `Grunnkurs Hypopressiv Trening` in GHL Memberships.
2. Create one Category per Kajabi module (skip the two draft-only modules unless the client
   wants them republished).
3. For each lesson: re-create title, pull lesson body HTML via
   `get_lesson(site_id: 171481, lesson_id: ...)` and paste into GHL lesson body.
4. Re-host video: download/export each Wistia asset (`wistia_id` in the course data) and
   upload natively to GHL, **or** keep Wistia hosting and embed the existing Wistia player
   via GHL's custom HTML embed block (faster, avoids re-encoding 48 videos).
5. Leave "Min historie" (draft) unpublished in GHL to match current Kajabi state.
6. Do not migrate MOTIVASJONSMAI / PANGSTART — they are stale live-event drafts. Flag to
   client for confirmation before deleting outright.

---

## 2. Grunnkurs Hypopressiv Trening + HypoGold (id 2148488003)

**Kajabi structure:** 20 modules, mixed publishing states, **real drip scheduling** on the
weekly modules (`publishing_state: "drip"`). This is the only one of the three courses with
drip — treat it differently from #1 and #3.

| Module | Lessons | Submodules | State |
|---|---|---|---|
| START HER / UKE 1: Oppstart + pusteteknikken | 7 | 1 | published |
| HYPO GOLD LIVE | 3 | 2 | published |
| Bonusbiblioteket | 16 | 0 | published |
| Uke 2 - 3: Stående og liggende | 4 | 2 | **drip** |
| Uke 4 - 5: Stående + på alle 4 | 2 | 3 | **drip** |
| Uke 6 - 7: Panna ned + asymmetrisk liggende | 3 | 4 | **drip** |
| Uke 8: Teknikk | 3 | 4 | **drip** |
| Uke 9: Skredderstilling | 3 | 4 | **drip** |
| Uke 10 - 11: Fremoverbøyd | 2 | 4 | **drip** |
| Uke 12: Grunnserien er på plass! | 3 | 4 | **drip** |
| VEIEN VIDERE: FÅ MER EFFEKT! | 1 | 5 | drip |
| VEIEN VIDERE: BLI STERKERE! | 1 | 6 | drip |
| VEIEN VIDERE: DITT BESTE LIV | 0 | 4 | **draft — skip** |
| HYPO GOLD - FAVORITTER | 0 | 6 | published (submodules only) |
| Uke 12: Veien videre #2 | 0 | 1 | **draft — skip** |
| Start her (old) | 4 | 0 | **draft — skip (legacy duplicate)** |
| Uke 1: Pusteteknikken (old) | 2 | 0 | **draft — skip (legacy duplicate)** |
| Uke 12: Veien videre #1 | 0 | 0 | **draft — skip** |
| MOTIVASJONSMAI | 2 | 0 | **draft — skip** |
| PANGSTART - alle sendinger | 5 | 0 | **draft — skip** |

### Steps
1. **Prune before migrating.** Six modules above are draft-only legacy/duplicate content
   ("(old)" modules, unused "Veien videre" variants, stale live-event recordings). Confirm
   with the client, then exclude these from the GHL rebuild — don't carry over dead weight.
2. Create course `Grunnkurs Hypopressiv Trening + HypoGold` in GHL.
3. Re-create the 3 non-drip modules first (Start her/Uke 1 combined, HYPO GOLD LIVE,
   Bonusbiblioteket) as always-unlocked categories, including their submodules — GHL
   supports one level of nested categories, matching Kajabi's module→submodule depth.
4. Re-create Uke 2 through Uke 12 (7 weekly modules) as **drip-scheduled categories**:
   - Map each week to a day-offset from enrollment (e.g. Uke 2-3 → day 7, Uke 4-5 → day 21,
     Uke 6-7 → day 35, Uke 8 → day 49, Uke 9 → day 56, Uke 10-11 → day 63, Uke 12 → day 77 —
     confirm exact Kajabi drip offsets in the admin UI before finalizing, since the API
     doesn't expose the drip interval directly).
   - Preserve their nested submodule structure.
5. Re-create "VEIEN VIDERE: FÅ MER EFFEKT!" and "BLI STERKERE!" (published, with
   submodules) as post-completion/next-step categories, drip-gated after Uke 12.
6. Re-create "HYPO GOLD - FAVORITTER" (submodule-only container) as a category housing its
   6 submodules of curated favorites.
7. Media: same Wistia re-host/embed decision as course #1 — this course has more video
   volume (~40+ lessons across active modules), so batch the export.
8. This course was linked to a Kajabi Offer ("Grunnkurs Hypopressiv Trening + HYPO GOLD",
   offer id `2149355028`) purely for access-gating — since pricing lives outside Kajabi,
   just confirm what event in the external payment platform should trigger GHL enrollment
   (e.g. webhook on purchase → GHL workflow grants course access), and rebuild that trigger
   in GHL, not the Kajabi offer itself.

---

## 3. Gravidkurs Hypopressiv Trening (id 702398)

**Kajabi structure:** 13 modules, ~30 lessons, no drip, one module has a nested submodule.

| Module | Lessons | Submodules | State |
|---|---|---|---|
| Start her | 5 | 0 | published (1 draft lesson: "Min historie") |
| Uke 1 - Biblioteket | 1 | 1 (Hverdagsteknikker, 4 lessons) | published |
| Uke 2 - 3: Pusten og underkroppen | 2 | 0 | published |
| Uke 4 - 5: Stillinger og overkropp | 2 | 0 | published |
| Uke 6 - 7: Panna ned + asymmetrisk liggende | 2 | 0 | published |
| Uke 8-9: Sittende / Squat prep | 2 | 0 | published |
| Uke 10 - 11: Teknikk og mer mobilitet | 2 | 0 | published |
| Uke 12: Sjekk hvor langt du har kommet | 2 | 0 | published (1 draft lesson) |
| Bonusmodul #1 - Hypnose for en bedre graviditet og fødsel | 4 | 0 | published (1 draft lesson: "Om hypnose") |
| Bonusmodul #2 - Forbered fødselen | 3 | 0 | published |
| Bonusmodul #3 - Få en bedre barseltid | 3 | 0 | published |

### Steps
1. Create course `Gravidkurs Hypopressiv Trening` in GHL.
2. Re-create modules 1:1 as categories, in the same order — no drip logic needed.
3. Re-create "Uke 1 - Biblioteket" with its nested "Hverdagsteknikker" submodule (4 lessons)
   — this is the only nesting in this course.
4. Leave the 3 draft lessons ("Min historie", one Uke 12 lesson, "Om hypnose") unpublished
   in GHL, matching Kajabi's current state, unless the client wants them finished/published
   as part of this migration.
5. Media re-host/embed decision same as above — lower volume here (~25 active videos).

---

## Cross-course notes

- **Courses #1 and #3 are structurally parallel** (general population vs. pregnancy-specific,
  same 12-week cadence, same "Learn"/"Practice" pattern). Consider building one GHL course
  template (category skeleton + lesson layout) and duplicating it for the second course to
  save rebuild time.
- **Only course #2 needs drip logic.** Don't add drip scheduling to #1 or #3 — they're
  meant to unlock in full on enrollment, matching current Kajabi behavior.
- **Pricing/checkout is not part of this migration.** Since Kajabi only hosts content here,
  GHL enrollment/access should be triggered by whatever event your external payment platform
  fires (webhook, Zapier, native integration) — not by a GHL native order form, unless you're
  also planning to consolidate checkout into GHL later (out of scope for this pass).
- **Legacy/draft cleanup:** Before migrating course #2 specifically, get explicit sign-off
  from the client on which draft/legacy modules to drop vs. carry over — don't silently
  migrate dead content.

## Suggested migration order

1. **Gravidkurs Hypopressiv Trening** (smallest, simplest, no drip) — validate the
   content-transfer + video-hosting process end-to-end on the lowest-risk course.
2. **Grunnkurs Hypopressiv Trening** (flagship, largest member base, still flat structure) —
   apply the same process at scale.
3. **Grunnkurs Hypopressiv Trening + HypoGold** (most complex: drip + legacy cleanup) —
   tackle last once the process is proven, and only after pruning is confirmed with the client.
