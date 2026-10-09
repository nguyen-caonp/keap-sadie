# Claude Code ↔ Keap Connection Plan

**Goal:** Let Claude Code read and (carefully) write Keap CRM data — contacts, tags, notes,
tasks, orders — through the Keap REST API v2 (<https://developer.infusionsoft.com/docs/restv2/>).
**Status:** Plan only. Nothing is built yet.

> **Verify before building.** The Keap developer site was unreachable from the session that
> wrote this plan. Auth, base URL and rate limits below come from Keap's
> [PAT & Service Account Key page](https://developer.keap.com/pat-and-sak). Endpoint paths,
> pagination parameter names and filter syntax are **assumptions**. Check each one against the
> REST v2 reference during Phase 0.

---

## 1. Approach

There is no Keap connector in the MCP registry, so we build a small one ourselves.

| Option | What it is | Verdict |
|---|---|---|
| A. Raw `curl` from Bash | Claude calls the API directly with a token in an env var | Fine for a one-off. No guardrails, and Claude has to re-learn the API every session |
| **B. Local MCP server (stdio)** | A small typed server exposing Keap operations as MCP tools | **Recommended.** Gives typed tools, central throttling, read-only by default, and a safety layer for writes |
| C. Remote MCP server (HTTP + OAuth) | The same server hosted, added as a custom connector in claude.ai | Later, only if non-Claude-Code surfaces (claude.ai, mobile) need Keap too |

Build B so that moving to C later only means changing the transport and the auth.

---

## 2. Authentication

| Method | Use when | Notes |
|---|---|---|
| **Personal Access Token (PAT)** | One Keap account, used by one person | Simplest. Created in the Keap developer portal and tied to a user |
| Service Account Key (SAK) | One Keap account, shared or automated use | Created in the Keap app settings by an admin. Not tied to a person. Preferred for a long-lived integration |
| OAuth2 (authorization code) | Several Keap accounts, or a hosted connector (option C) | Needs a registered developer app, a refresh-token store and token rotation |

- Header: `Authorization: Bearer <key>`
- Base URL: `https://api.infusionsoft.com/crm/rest/v2`
- Keep the key in `KEAP_API_KEY`. **Never commit it.** Keap says to treat the key like a
  password.
- **Phase 1 decision:** use a SAK if a Keap admin can issue one, otherwise a PAT.

---

## 3. API constraints to design around

- **Rate limits (PAT/SAK):** 10 requests per second, 240 per minute, 30,000 per day. OAuth
  apps get higher quotas.
  - The server uses a token-bucket throttle of about 8 requests per second and 200 per minute.
  - It retries `429` and `5xx` responses with exponential backoff and honours `Retry-After`.
  - It logs the daily count so a runaway loop can't burn the quota.
- **Pagination:** v2 is cursor-based. The assumed parameters are `page_size` and
  `page_token`, and responses are assumed to return `next_page_token`. *Verify this.* Tools
  return one page plus the cursor and never auto-fetch everything. A `max_records` cap stops
  Claude from pulling the whole database into context.
- **Filtering:** v2 list endpoints take a `filter` query string and an `order_by` parameter.
  *Verify the syntax for each endpoint.*
- **PII:** contact records hold emails, phone numbers and addresses. Tools return trimmed field
  sets by default and full records only on request.

---

## 4. Tool surface (MVP → later)

Assumed v2 resource paths are in brackets. Confirm every path in Phase 0.

**Phase 1 — read-only**
- `keap_search_contacts(query?, email?, tag_id?, page_size?, page_token?)` → `GET /contacts`
- `keap_get_contact(contact_id, fields?)` → `GET /contacts/{id}`
- `keap_list_tags(category?, page_token?)` → `GET /tags`
- `keap_list_tagged_contacts(tag_id, page_token?)` → `GET /tags/{id}/contacts`
- `keap_list_notes(contact_id)` and `keap_list_tasks(contact_id?)`
- `keap_list_orders(contact_id?)` and `keap_list_subscriptions(contact_id?)`
- `keap_list_custom_fields(entity)`, used to map custom field IDs to names

**Phase 2 — writes, behind a flag**
- `keap_create_contact`, `keap_update_contact` (an upsert by email, if v2 supports it)
- `keap_apply_tags`, `keap_remove_tags`. Applying tags can **trigger Keap automations and
  send email**, so treat these as high-impact.
- `keap_create_note`, `keap_create_task`

**Deliberately excluded:** deletes, merges, payment and charge endpoints, email sending, and
user or permission management. Add them only if a concrete need comes up.

---

## 5. Safety model

1. The server starts in **read-only mode**. Write tools register only when
   `KEAP_ALLOW_WRITES=1` is set.
2. Write tools support `dry_run: true`, which is the default. A dry run returns the exact HTTP
   request it would send. A second call with `dry_run: false` executes it.
3. Claude Code permissions stay on "ask" for `mcp__keap__*` write tools (in
   `.claude/settings.json`), so a human approves every mutation. Read tools can be added to
   `allow`.
4. Bulk guard: a single call refuses to modify more than N contacts. N defaults to 25.
5. Every write is logged as one JSON line (time, tool, contact IDs, payload hash) to
   `~/.keap-mcp/audit.log`.
6. Test against a **Keap sandbox or trial app** first, never the live client account.

---

## 6. Implementation

**Stack:** TypeScript with `@modelcontextprotocol/sdk` and `zod` for schemas, plus native
`fetch`. Python with FastMCP and `httpx` works equally well. Pick whichever the maintainer
prefers.

```
keap-mcp/
  src/
    index.ts          # MCP server bootstrap (stdio), tool registration, read-only gate
    keapClient.ts     # fetch wrapper: base URL, auth header, throttle, retry, pagination
    tools/contacts.ts
    tools/tags.ts
    tools/notes-tasks.ts
    tools/commerce.ts # orders, subscriptions (read-only)
  test/               # unit tests with mocked HTTP; one opt-in live smoke test
  .env.example        # KEAP_API_KEY=, KEAP_ALLOW_WRITES=0
  README.md
```

**Register with Claude Code** at project scope, in a committed `.mcp.json` that holds no
secret:

```json
{
  "mcpServers": {
    "keap": {
      "command": "node",
      "args": ["keap-mcp/dist/index.js"],
      "env": { "KEAP_API_KEY": "${KEAP_API_KEY}", "KEAP_ALLOW_WRITES": "${KEAP_ALLOW_WRITES:-0}" }
    }
  }
}
```

The one-off equivalent is
`claude mcp add keap -e KEAP_API_KEY=$KEAP_API_KEY -- node keap-mcp/dist/index.js`.

**Claude Code on the web (cloud sessions):**
- The environment's network policy must allow `api.infusionsoft.com`. It currently blocks
  `developer.infusionsoft.com`, so assume the API host is blocked too.
- Add `KEAP_API_KEY` as an environment secret.
- A SessionStart hook or setup script has to build `keap-mcp` (`npm ci && npm run build`).

---

## 7. Milestones

| # | Milestone | Done when |
|---|---|---|
| 0 | **Verify the API.** Read the REST v2 reference. Confirm paths, pagination, filters and tag-application semantics. Get a sandbox and a key | A short "verified" table replaces the assumptions in §3–4 |
| 1 | **Spike.** `curl` `GET /contacts?page_size=1` with the key | A 200 response and a real response shape saved as a test fixture |
| 2 | **Read-only MCP.** Client, throttle and the Phase 1 tools, with unit tests | Claude Code answers "find contact X and list their tags and orders" against the sandbox |
| 3 | **Writes.** The Phase 2 tools with dry-run, flag, bulk guard and audit log | A tag applied to a sandbox contact via Claude, with approval prompt and audit entry confirmed |
| 4 | **Rollout.** Live key, permissions config, README and a cloud environment if needed | Used on the real account for one read-only workflow |
| 5 | *(optional)* **Remote connector.** HTTP transport plus OAuth2 | Usable from claude.ai |

---

## 8. Open questions for the client

1. Which Keap account(s) does this cover? Can an admin issue a Service Account Key?
2. What are the first 2–3 jobs Claude should do? For example: look up a customer, segment by
   tag, clean up tags, or sync course buyers. These decide which Phase 1 tools matter most.
3. Is a Keap sandbox or trial app available for testing?
4. Should Claude ever write to the live account? If so, which writes count as acceptable?
5. Is there a cross-system workflow to support? For example, matching Kajabi or Go High Level
   members to Keap contacts, which links to the migration in
   `kajabi-to-ghl-course-migration.md`.
