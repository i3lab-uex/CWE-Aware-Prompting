from __future__ import annotations

import json
from typing import Any, Dict

def validate_and_parse_json(incoming_req: Dict[str, Any]) -> Dict[str, Any]:
    """
    Validate and parse a JSON request.

    Parameters
    ----------
    incoming_req : dict
        Dictionary containing at least the keys ``headers`` and ``body``.
        * ``headers`` should be a mapping of header names to values.
        * ``body`` can be either a string or bytes representing the raw request body.

    Returns
    -------
    dict
        The parsed JSON payload as a Python dictionary.

    Raises
    ------
    ValueError
        If the Content-Type header is missing or not JSON-compatible.
        If the body cannot be parsed as valid JSON.

    Notes
    -----
    * The function is intentionally conservative: it only accepts headers that
      explicitly declare a JSON-compatible MIME type. This mitigates risks from
      content sniffing attacks (CWE‑693).
    * The body is decoded using UTF-8 if it is bytes, which is the default
      encoding for HTTP payloads.
    """
    # Extract headers and body, providing defaults if missing
    headers = incoming_req.get("headers", {})
    body = incoming_req.get("body")

    if body is None:
        raise ValueError("Missing request body")

    # Normalise header names to lowercase for case-insensitive lookup
    headers_lower = {k.lower(): v for k, v in headers.items()}

    content_type = headers_lower.get("content-type")
    if not content_type or "application/json" not in content_type.lower():
        raise ValueError("Content-Type must be application/json")

    # Decode bytes to string if necessary
    if isinstance(body, bytes):
        try:
            body_str = body.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise ValueError("Body is not valid UTF-8") from exc
    elif isinstance(body, str):
        body_str = body
    else:
        raise ValueError("Body must be a string or bytes")

    # Parse JSON safely
    try:
        parsed = json.loads(body_str)
    except json.JSONDecodeError as exc:
        raise ValueError("Malformed JSON") from exc

    if not isinstance(parsed, dict):
        # The API expects a JSON object; reject arrays or primitives
        raise ValueError("JSON body must be an object (dictionary)")

    return parsed