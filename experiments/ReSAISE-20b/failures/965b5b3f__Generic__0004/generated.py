import json
from typing import Dict, Any


def process_json_request(req_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Parse and validate a JSON request body.

    Parameters
    ----------
    req_data : dict
        A dictionary expected to contain the request ``headers`` and ``body``.
        * ``headers`` : Mapping of header names to values (case‑insensitive).
        * ``body``    : Raw request body, either a bytes object or a string.

    Returns
    -------
    dict
        The parsed JSON payload.

    Raises
    ------
    ValueError
        If the Content‑Type is missing or not JSON.
        If the body cannot be decoded as valid JSON.
    """
    # ---- Content‑Type validation -----------------------------------------
    headers = req_data.get("headers", {})
    if not isinstance(headers, dict):
        raise ValueError("Request headers must be a dictionary")

    # Normalize header keys to lower case for case‑insensitive matching
    content_type = None
    for key, value in headers.items():
        if key.lower() == "content-type":
            content_type = value
            break

    if not content_type or "application/json" not in content_type.lower():
        raise ValueError(
            f"Unsupported Content-Type: {content_type!r}. Expected application/json."
        )

    # ---- Body extraction and JSON decoding --------------------------------
    body = req_data.get("body")
    if body is None:
        raise ValueError("Request body missing")

    # Accept both bytes and string representations
    if isinstance(body, bytes):
        try:
            body_str = body.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise ValueError(f"Body decoding error: {exc}") from exc
    elif isinstance(body, str):
        body_str = body
    else:
        raise ValueError(f"Unsupported body type: {type(body).__name__}")

    try:
        payload = json.loads(body_str)
    except json.JSONDecodeError as exc:
        raise ValueError(f"Invalid JSON payload: {exc}") from exc

    if not isinstance(payload, dict):
        raise ValueError("JSON payload must be an object (dict)")

    return payload