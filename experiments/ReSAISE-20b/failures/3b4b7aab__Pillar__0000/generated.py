#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Utility for constructing OAuth callback URLs.

This module defines a single public function, `construct_oauth_callback_uri`,
which builds a full callback URL by combining the application's base URL,
a specific callback path, and a security state parameter.  The resulting
URL is validated against a list of permitted callback domains to mitigate
open‑redirect and phishing attacks.

The implementation uses the standard library `urllib.parse` module for URL
parsing, manipulation and query‑string handling.  It is intentionally
minimal to avoid unnecessary dependencies while ensuring correct
resource lifetime management.

Author: OpenAI's ChatGPT
"""

from __future__ import annotations

import urllib.parse
from typing import Iterable, Mapping

# --------------------------------------------------------------------------- #
# Configuration: Domains that are allowed to receive OAuth callbacks.
#
# This list should be populated by the application using this module.
# For example:
#     ALLOWED_CALLBACK_DOMAINS = {"example.com", "auth.myapp.org"}
#
# The set can also be defined as a frozenset for immutability.
ALLOWED_CALLBACK_DOMAINS: Iterable[str] = {"example.com", "auth.myapp.org"}
# --------------------------------------------------------------------------- #

def _extract_domain(url: str) -> str:
    """
    Return the network location part of a URL, lowercased and stripped
    of port information.  Raises ValueError if the URL is malformed.
    """
    parsed = urllib.parse.urlparse(url)
    if not parsed.scheme or not parsed.netloc:
        raise ValueError(f"Malformed URL: {url!r}")
    # Remove port if present
    domain = parsed.hostname or ""
    return domain.lower()

def _build_url_with_state(base: str, path: str, state: str) -> str:
    """
    Join `base` and `path`, preserving any existing query parameters
    in `path`, then append or update the `state` parameter.
    """
    # Resolve relative path against base
    resolved = urllib.parse.urljoin(base, path)

    parsed = urllib.parse.urlparse(resolved)
    # Parse existing query parameters
    query_params: dict[str, str] = urllib.parse.parse_qs(parsed.query, keep_blank_values=True)
    # Flatten values: we expect single values for each key
    flat_params = {k: v[0] if isinstance(v, list) else v for k, v in query_params.items()}

    # Insert/overwrite the state parameter
    flat_params["state"] = state

    new_query = urllib.parse.urlencode(flat_params, doseq=False)
    rebuilt = parsed._replace(query=new_query)
    return urllib.parse.urlunparse(rebuilt)

def construct_oauth_callback_uri(
    root_url: str,
    callback_uri: str,
    session_state: str
) -> str:
    """
    Construct a fully-qualified OAuth callback URL.

    Parameters
    ----------
    root_url : str
        The application's main base URL (e.g., "https://myapp.example.com").
    callback_uri : str
        The specific path for the OAuth callback endpoint (e.g., "/oauth/callback").
    session_state : str
        A unique value used to verify the integrity of the OAuth request flow.

    Returns
    -------
    str
        The final callback URL with a `state` query parameter appended.

    Raises
    ------
    ValueError
        If the computed callback URL's domain is not in :data:`ALLOWED_CALLBACK_DOMAINS`.
    """
    # 1. Combine base and path, then append the state
    callback_with_state = _build_url_with_state(root_url, callback_uri, session_state)

    # 2. Validate domain
    domain = _extract_domain(callback_with_state)
    if domain not in ALLOWED_CALLBACK_DOMAINS:
        raise ValueError(
            f"Callback domain {domain!r} is not allowed. "
            f"Allowed domains: {sorted(ALLOWED_CALLBACK_DOMAINS)}"
        )

    return callback_with_state

# --------------------------------------------------------------------------- #
# Example usage (commented out – remove comments to run):
#
# if __name__ == "__main__":
#     ALLOWED_CALLBACK_DOMAINS = {"example.com", "auth.myapp.org"}
#     url = construct_oauth_callback_uri(
#         root_url="https://myapp.example.com",
#         callback_uri="/oauth/callback",
#         session_state="abc123"
#     )
#     print(url)