import json
from typing import Dict, Any

# Standard HTTP header keys are case‑insensitive.  We normalise them to lower case.
def _get_header_value(headers: Dict[str, Any], key: str) -> str | None:
    """Return the header value for *key* in a case‑insensitive manner."""
    lower_key = key.lower()
    for h, v in headers.items():
        if h.lower() == lower_key:
            return str(v)
    return None


def decode_json_request(req: Dict[str, Any]) -> Dict[str, Any]:
    """
    Parse and validate the body of an incoming JSON request.

    Parameters
    ----------
    req : dict
        A dictionary containing at least the keys 'headers' and 'body'.
        * headers* should be a mapping of header names to values.
        * body* is expected to be a byte string or text containing JSON.

    Returns
    -------
    dict
        The decoded JSON payload as a Python dictionary.

    Raises
    ------
    ValueError
        If the content type is not acceptable or if JSON decoding fails.
    """
    # 1. Validate presence of required keys
    if not isinstance(req, dict):
        raise ValueError("Request must be a dictionary")

    headers = req.get("headers")
    body = req.get("body")

    if headers is None or body is None:
        raise ValueError("Request must contain 'headers' and 'body' keys")

    # 2. Check content type
    content_type = _get_header_value(headers, "Content-Type")
    if not content_type or not content_type.lower().startswith("application/json"):
        raise ValueError(
            "Unsupported media type. Expected 'application/json' content type"
        )

    # 3. Decode body
    try:
        if isinstance(body, bytes):
            body_text = body.decode("utf-8")
        else:
            body_text = str(body)
    except Exception as exc:  # pragma: no cover
        raise ValueError("Failed to decode request body") from exc

    try:
        payload = json.loads(body_text)
    except json.JSONDecodeError as exc:
        raise ValueError(f"Invalid JSON payload: {exc.msg}") from exc

    if not isinstance(payload, dict):
        raise ValueError("JSON payload must be an object (dict)")

    return payload