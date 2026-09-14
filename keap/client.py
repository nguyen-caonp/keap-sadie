"""Thin client for the Keap (formerly Infusionsoft) REST API v1.

Docs: https://developer.keap.com/docs/rest/ (mirrored at
https://developer.infusionsoft.com/docs/rest/)

Auth: reads the API key from the KEAP_API_KEY environment variable and
sends it as a Bearer token. Never hardcode the key in source.
"""

from __future__ import annotations

import os
from typing import Any, Iterator

import requests

BASE_URL = "https://api.infusionsoft.com/crm/rest/v1"


class KeapError(RuntimeError):
    pass


class KeapClient:
    def __init__(self, api_key: str | None = None, base_url: str = BASE_URL):
        self.api_key = api_key or os.environ.get("KEAP_API_KEY")
        if not self.api_key:
            raise KeapError(
                "No Keap API key found. Set the KEAP_API_KEY environment variable."
            )
        self.base_url = base_url.rstrip("/")
        self.session = requests.Session()
        self.session.headers.update(
            {
                "Authorization": f"Bearer {self.api_key}",
                "Accept": "application/json",
            }
        )

    def _request(self, method: str, path: str, **kwargs: Any) -> dict:
        url = f"{self.base_url}{path}"
        resp = self.session.request(method, url, timeout=30, **kwargs)
        if not resp.ok:
            raise KeapError(f"{method} {path} -> {resp.status_code}: {resp.text}")
        if resp.content:
            return resp.json()
        return {}

    # ---- Contacts -----------------------------------------------------

    def list_contacts(
        self, limit: int = 50, offset: int = 0, email: str | None = None
    ) -> dict:
        params: dict[str, Any] = {"limit": limit, "offset": offset}
        if email:
            params["email"] = email
        return self._request("GET", "/contacts", params=params)

    def iter_all_contacts(self, page_size: int = 100) -> Iterator[dict]:
        offset = 0
        while True:
            page = self.list_contacts(limit=page_size, offset=offset)
            contacts = page.get("contacts", [])
            if not contacts:
                return
            yield from contacts
            offset += page_size
            if offset >= page.get("count", offset):
                return

    def get_contact(self, contact_id: int) -> dict:
        return self._request("GET", f"/contacts/{contact_id}")

    # ---- Tags -----------------------------------------------------------

    def list_tags(self, limit: int = 50, offset: int = 0) -> dict:
        params = {"limit": limit, "offset": offset}
        return self._request("GET", "/tags", params=params)

    def iter_all_tags(self, page_size: int = 100) -> Iterator[dict]:
        offset = 0
        while True:
            page = self.list_tags(limit=page_size, offset=offset)
            tags = page.get("tags", [])
            if not tags:
                return
            yield from tags
            offset += page_size
            if offset >= page.get("count", offset):
                return

    def list_contact_tags(self, contact_id: int) -> dict:
        return self._request("GET", f"/contacts/{contact_id}/tags")

    def apply_tags(self, contact_id: int, tag_ids: list[int]) -> dict:
        return self._request(
            "POST",
            f"/contacts/{contact_id}/tags",
            json={"tagIds": tag_ids},
        )

    def remove_tag(self, contact_id: int, tag_id: int) -> None:
        self._request("DELETE", f"/contacts/{contact_id}/tags/{tag_id}")
