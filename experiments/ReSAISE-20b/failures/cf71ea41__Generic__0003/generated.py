#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Utility for validating and parsing JSON payloads in FastAPI handlers.

The function `process_json_payload` accepts a dictionary that mimics the
structure of FastAPI's request object (`request.headers`, `request.body()`).
It verifies that the Content-Type header indicates a JSON-compatible
media type and attempts to parse the request body.  Malformed JSON or an
inappropriate Content-Type results in a `ValueError`.

This module is intentionally lightweight and does not depend on FastAPI
directly, making it easy to unit‑test or reuse in other contexts.
"""

from __future__ import annotations

import json
from typing import Any, Dict

# Define a list of acceptable JSON media types.  This can be extended
# if the application needs to support more variations (e.g., "application/json-patch+json").
_ACCEPTABLE_CONTENT_TYPES = (
    "application/json",
    "application/ld+json",
    "application/vnd.api+json",
)


def _is_json_content_type(content_type: str | None) -> bool:
    """
    Determine whether the supplied content type string is acceptable for JSON.

    Parameters
    ----------
    content_type : str | None
        The value of the `Content-Type` header.  It may be ``None`` if the
        header is missing.

    Returns
    -------
    bool
        True if the content type indicates JSON, False otherwise.
    """
    if not content_type:
        return False
    # Normalize: strip parameters (e.g., "; charset=utf-8")
    media_type = content_type.split(";", 1)[0].strip().lower()
    return media_type in _ACCEPTABLE_CONTENT_TYPES


def process_json_payload(req_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Validate and parse the JSON body of an HTTP request.

    Parameters
    ----------
    req_data : dict
        Dictionary containing at least the keys ``headers`` and ``body``.
        ``headers`` should itself be a mapping (e.g., dict or Starlette
        Headers object) where the key ``Content-Type`` is case‑insensitive.
        ``body`` can be a bytes object or a string.  If it is a string,
        it will be encoded as UTF‑8 before parsing.

    Returns
    -------
    dict
        The parsed JSON object (Python dictionary).

    Raises
    ------
    ValueError
        If the request does not contain a JSON-compatible Content-Type.
    ValueError
        If the body cannot be decoded as valid JSON.

    Notes
    -----
    - The function deliberately does **not** attempt to parse other content
      types such as XML or plain text.
    - It performs minimal size checking to guard against extremely large
      payloads that could exhaust memory.  Adjust ``max_body_size`` if
      needed for your environment.
    """
    # Extract headers and body from the request dictionary
    headers = req_data.get("headers", {})
    if isinstance(headers, dict):
        # Headers may be case‑insensitive; normalize to lower‑case keys
        headers = {k.lower(): v for k, v in headers.items()}
    else:
        # If not a dict (e.g., Starlette Headers), convert to dict
        headers = {k.lower(): v for k, v in headers}

    content_type = headers.get("content-type")

    if not _is_json_content_type(content_type):
        raise ValueError(
            f"Unsupported Content-Type '{content_type}'. Expected JSON-compatible type."
        )

    body = req_data.get("body", b"")

    # Ensure the body is in bytes for json.loads
    if isinstance(body, str):
        body_bytes = body.encode("utf-8")
    elif isinstance(body, bytes):
        body_bytes = body
    else:
        raise ValueError("Request body must be a string or bytes.")

    # Optional: enforce a maximum size (e.g., 5 MB) to prevent denial‑of‑service
    max_body_size = 5 * 1024 * 1024  # 5 MB
    if len(body_bytes) > max_body_size:
        raise ValueError("Request body too large.")

    try:
        # json.loads expects a str, so decode
        decoded_body = body_bytes.decode("utf-8")
        parsed_json: Any = json.loads(decoded_body)
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ValueError(f"Malformed JSON payload: {exc}") from exc

    if not isinstance(parsed_json, dict):
        raise ValueError(
            f"JSON payload must be an object (dict), got {type(parsed_json).__name__}."
        )

    return parsed_json