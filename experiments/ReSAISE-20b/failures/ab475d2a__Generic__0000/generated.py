import json
from typing import Dict, Any


def decode_json_request(req: Dict[str, Any]) -> Dict[str, Any]:
    """
    Parse and validate the body of an incoming JSON request.

    Parameters
    ----------
    req : dict
        A dictionary containing at least the keys ``headers`` and ``body``.
        * ``headers`` should be a mapping of header names to values (case‑insensitive).
        * ``body`` can be either a `bytes` or `str` object containing the raw request payload.

    Returns
    -------
    dict
        The decoded JSON payload as a Python dictionary.

    Raises
    ------
    ValueError
        If the ``Content-Type`` header is missing or does not indicate JSON.
        If the body cannot be decoded as valid JSON.
    """
    # Helper to normalize header names (case‑insensitive)
    def _get_header(name: str) -> str | None:
        for key, value in req.get("headers", {}).items():
            if key.lower() == name.lower():
                return value
        return None

    content_type = _get_header("Content-Type")
    if not content_type or "application/json" not in content_type.lower():
        raise ValueError("Unsupported Content-Type: only 'application/json' is allowed")

    raw_body = req.get("body")
    if raw_body is None:
        raise ValueError("Missing request body")

    # Ensure we have a string to parse
    if isinstance(raw_body, bytes):
        try:
            body_str = raw_body.decode("utf-8")
        except Exception as exc:  # pragma: no cover
            raise ValueError(f"Body decoding failed: {exc}") from exc
    elif isinstance(raw_body, str):
        body_str = raw_body
    else:  # pragma: no cover
        raise ValueError(f"Unsupported body type: {type(raw_body).__name__}")

    # Strip whitespace to allow empty JSON objects
    body_str = body_str.strip()
    if not body_str:
        return {}

    try:
        decoded = json.loads(body_str)
    except json.JSONDecodeError as exc:
        raise ValueError(f"Invalid JSON payload: {exc}") from exc

    if not isinstance(decoded, dict):
        raise ValueError("JSON payload must be an object (dict)")

    return decoded