import json
from typing import Dict, Any

def process_json_payload(req_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Parse and validate a JSON payload from an HTTP request.

    Parameters
    ----------
    req_data : dict
        Dictionary containing at least the keys ``headers`` and ``body``.
        ``headers`` should be a mapping of header names to values,
        and ``body`` can be either a JSON string or already parsed data.

    Returns
    -------
    dict
        The validated request body as a Python dictionary.

    Raises
    ------
    ValueError
        If the content‑type is not JSON compatible.
        If the body cannot be decoded as valid JSON.
    """
    # Extract headers and body
    headers = req_data.get("headers", {})
    body = req_data.get("body")

    # Normalise header keys to lowercase for case‑insensitive lookup
    headers_lc = {k.lower(): v for k, v in headers.items()}

    # Verify content‑type
    ct = headers_lc.get("content-type", "")
    if not any(fmt in ct.lower() for fmt in ("application/json", "application/*+json")):
        raise ValueError(f"Unsupported content-type: {ct!r}")

    # If body is already a dict/list, ensure it's a dict
    if isinstance(body, (dict, list)):
        if isinstance(body, list):
            raise ValueError("JSON body must be an object (dict), not a list.")
        return body

    # Body should be a string or bytes
    if isinstance(body, (bytes, bytearray)):
        body_text = body.decode("utf-8")
    elif isinstance(body, str):
        body_text = body
    else:
        raise ValueError(f"Unsupported body type: {type(body).__name__}")

    # Parse JSON
    try:
        parsed = json.loads(body_text)
    except json.JSONDecodeError as exc:
        raise ValueError(f"Malformed JSON: {exc}") from exc

    # Ensure the parsed payload is a dict
    if not isinstance(parsed, dict):
        raise ValueError("JSON body must be an object (dict), not a list or scalar.")

    return parsed