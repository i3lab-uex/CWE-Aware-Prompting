import json
from typing import Any, Dict


def process_json_input(req: Dict[str, Any]) -> Dict[str, Any]:
    """
    Parse a JSON request body from a FastAPI-like request dictionary.

    Parameters
    ----------
    req : dict
        Dictionary containing the HTTP headers and body of an incoming request.
        Expected keys:
            - 'headers': a mapping of header names to values (case-insensitive).
            - 'body'   : the raw request body, expected to be a JSON string.

    Returns
    -------
    dict
        The parsed JSON payload as a Python dictionary.

    Raises
    ------
    ValueError
        If the 'Content-Type' header is missing or not set to 'application/json'.
        If the body cannot be decoded as valid JSON.
    """
    # Retrieve headers, normalising keys to lowercase for case‑insensitive lookup
    raw_headers = req.get("headers", {})
    if not isinstance(raw_headers, dict):
        raise ValueError("Headers must be a dictionary")

    headers = {k.lower(): v for k, v in raw_headers.items()}

    # Validate Content-Type
    content_type = headers.get("content-type")
    if content_type is None:
        raise ValueError("Missing Content-Type header")

    # Accept only application/json or a variant with charset
    if not content_type.lower().startswith("application/json"):
        raise ValueError(
            f"Invalid Content-Type '{content_type}'. Expected 'application/json'"
        )

    # Retrieve body
    raw_body = req.get("body", "")
    if not isinstance(raw_body, str):
        raise ValueError("Body must be a string")

    # Parse JSON
    try:
        payload = json.loads(raw_body)
    except json.JSONDecodeError as exc:
        raise ValueError(f"Malformed JSON: {exc.msg}") from exc

    if not isinstance(payload, dict):
        raise ValueError("JSON payload must be an object (dictionary)")

    return payload