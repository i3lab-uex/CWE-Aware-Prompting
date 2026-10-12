import json
from typing import Dict, Any

def handle_json_input(client_request: Dict[str, Any]) -> Dict[str, Any]:
    """
    Parse and validate a JSON request body.

    Parameters
    ----------
    client_request : dict
        Dictionary containing at least two keys:
            * ``headers``: a mapping of HTTP header names to values.
            * ``body``   : the raw request payload as a string.

    Returns
    -------
    dict
        The parsed JSON object from the request body.

    Raises
    ------
    ValueError
        If the Content-Type header is missing or not JSON-compatible.
        If the body cannot be decoded as valid JSON.
    """
    # ---- 1. Validate headers ------------------------------------------------
    headers = client_request.get("headers", {})
    if not isinstance(headers, dict):
        raise ValueError("Headers must be a dictionary")

    # HTTP header names are case‑insensitive; normalise to lowercase
    content_type = headers.get("Content-Type") or headers.get("content-type")
    if not content_type:
        raise ValueError("Missing Content-Type header")

    # Accept common JSON media types
    json_media_types = {
        "application/json",
        "application/json; charset=utf-8",
        "application/json;charset=utf-8",
    }
    if not any(content_type.lower().startswith(mt) for mt in json_media_types):
        raise ValueError(f"Unsupported Content-Type: {content_type}")

    # ---- 2. Validate and parse body ----------------------------------------
    raw_body = client_request.get("body")
    if raw_body is None:
        raise ValueError("Missing request body")

    # Ensure the body is a string; FastAPI typically gives str, but guard against bytes
    if isinstance(raw_body, bytes):
        try:
            raw_body = raw_body.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise ValueError("Request body is not valid UTF-8") from exc

    if not isinstance(raw_body, str):
        raise ValueError("Request body must be a string")

    try:
        parsed = json.loads(raw_body)
    except json.JSONDecodeError as exc:
        raise ValueError(f"Malformed JSON: {exc.msg}") from exc

    if not isinstance(parsed, dict):
        raise ValueError("JSON payload must be an object (dictionary)")

    return parsed