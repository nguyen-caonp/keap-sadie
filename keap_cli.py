#!/usr/bin/env python3
"""CLI for common Keap tasks: pull contact/tag reports, inspect a contact's
tags, and apply/remove tags.

Requires KEAP_API_KEY to be set in the environment. See .env.example.

Examples:
    python3 keap_cli.py list-tags
    python3 keap_cli.py list-contacts --limit 20
    python3 keap_cli.py contact-tags 123
    python3 keap_cli.py apply-tag 123 456
    python3 keap_cli.py remove-tag 123 456
    python3 keap_cli.py report --tag-name "Customer" --out report.csv
"""

from __future__ import annotations

import argparse
import csv
import sys

from keap.client import KeapClient, KeapError


def cmd_list_tags(client: KeapClient, args: argparse.Namespace) -> None:
    for tag in client.iter_all_tags():
        print(f"{tag['id']}\t{tag['name']}\t{tag.get('category', {}).get('name', '')}")


def cmd_list_contacts(client: KeapClient, args: argparse.Namespace) -> None:
    page = client.list_contacts(limit=args.limit, email=args.email)
    for c in page.get("contacts", []):
        email = next(
            (e["email"] for e in c.get("email_addresses", []) if e.get("email")), ""
        )
        print(f"{c['id']}\t{c.get('given_name', '')} {c.get('family_name', '')}\t{email}")


def cmd_contact_tags(client: KeapClient, args: argparse.Namespace) -> None:
    data = client.list_contact_tags(args.contact_id)
    tags = data.get("tags", [])
    if not tags:
        print("No tags applied to this contact.")
        return
    for t in tags:
        tag = t.get("tag", t)
        print(f"{tag.get('id')}\t{tag.get('name')}")


def cmd_apply_tag(client: KeapClient, args: argparse.Namespace) -> None:
    client.apply_tags(args.contact_id, [args.tag_id])
    print(f"Applied tag {args.tag_id} to contact {args.contact_id}.")


def cmd_remove_tag(client: KeapClient, args: argparse.Namespace) -> None:
    client.remove_tag(args.contact_id, args.tag_id)
    print(f"Removed tag {args.tag_id} from contact {args.contact_id}.")


def cmd_report(client: KeapClient, args: argparse.Namespace) -> None:
    tag_id = args.tag_id
    if args.tag_name and tag_id is None:
        match = next(
            (t for t in client.iter_all_tags() if t["name"].lower() == args.tag_name.lower()),
            None,
        )
        if not match:
            print(f"No tag named {args.tag_name!r} found.", file=sys.stderr)
            sys.exit(1)
        tag_id = match["id"]

    rows = []
    for c in client.iter_all_contacts():
        if tag_id is not None:
            contact_tags = client.list_contact_tags(c["id"]).get("tags", [])
            tag_ids = {t.get("tag", t).get("id") for t in contact_tags}
            if tag_id not in tag_ids:
                continue
        email = next(
            (e["email"] for e in c.get("email_addresses", []) if e.get("email")), ""
        )
        rows.append(
            {
                "id": c["id"],
                "given_name": c.get("given_name", ""),
                "family_name": c.get("family_name", ""),
                "email": email,
            }
        )

    with open(args.out, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["id", "given_name", "family_name", "email"])
        writer.writeheader()
        writer.writerows(rows)
    print(f"Wrote {len(rows)} contacts to {args.out}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Keap CLI")
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("list-tags", help="List all tags").set_defaults(func=cmd_list_tags)

    p = sub.add_parser("list-contacts", help="List contacts")
    p.add_argument("--limit", type=int, default=50)
    p.add_argument("--email", default=None)
    p.set_defaults(func=cmd_list_contacts)

    p = sub.add_parser("contact-tags", help="List tags applied to a contact")
    p.add_argument("contact_id", type=int)
    p.set_defaults(func=cmd_contact_tags)

    p = sub.add_parser("apply-tag", help="Apply a tag to a contact")
    p.add_argument("contact_id", type=int)
    p.add_argument("tag_id", type=int)
    p.set_defaults(func=cmd_apply_tag)

    p = sub.add_parser("remove-tag", help="Remove a tag from a contact")
    p.add_argument("contact_id", type=int)
    p.add_argument("tag_id", type=int)
    p.set_defaults(func=cmd_remove_tag)

    p = sub.add_parser("report", help="Export contacts (optionally filtered by tag) to CSV")
    p.add_argument("--tag-id", type=int, default=None)
    p.add_argument("--tag-name", default=None)
    p.add_argument("--out", default="report.csv")
    p.set_defaults(func=cmd_report)

    args = parser.parse_args()
    try:
        client = KeapClient()
    except KeapError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

    try:
        args.func(client, args)
    except KeapError as e:
        print(f"Keap API error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
