import json
from typing import Dict, Any

def handle_json_input(client_request: Dict[str, Any]) -> Dict:
    """
    Parse and validate a JSON request body.

    Parameters
    ----------
    client_request : dict
        Dictionary containing the HTTP request.  Expected keys are:
            - 'headers': a mapping of header names to values.
            - 'body'   : the raw request body (str or bytes).

    Returns
    -------
    dict
        The parsed JSON object.

    Raises
    ------
    ValueError
        If the request does not declare a JSON-compatible content type.
    ValueError
        If the body cannot be parsed as valid JSON.
    """
    # ------------------------------------------------------------------
    # 1. Verify Content-Type header
    # ------------------------------------------------------------------
    headers = client_request.get("headers", {})
    if not isinstance(headers, dict):
        raise ValueError("Headers must be a dictionary.")

    # Normalize header names to lowercase for case‑insensitive lookup
    content_type = next(
        (v for k, v in headers.items() if k.lower() == "content-type"),
        None,
    )
    if not content_type or not any(
        ct in content_type.lower()
        for ct in ("application/json", "application/ld+json", "application/vnd.api+json")
    ):
        raise ValueError("Content-Type must be JSON-compatible.")

    # ------------------------------------------------------------------
    # 2. Parse body
    # ------------------------------------------------------------------
    raw_body = client_request.get("body", "")
    if isinstance(raw_body, bytes):
        try:
            raw_body = raw_body.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise ValueError("Body contains invalid UTF‑8") from exc

    if not isinstance(raw_body, str):
        raise ValueError("Body must be a string or bytes.")

    try:
        parsed = json.loads(raw_body)
    except json.JSONDecodeError as exc:
        raise ValueError("Malformed JSON") from exc

    if not isinstance(parsed, dict):
        raise ValueError("JSON body must be an object (dict).")

    return parsed