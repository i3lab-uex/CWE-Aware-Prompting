import json
from typing import Dict, Any

def process_json_request(req_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Parse and validate a JSON request body.

    Parameters
    ----------
    req_data : dict
        Dictionary containing at least the keys 'headers' and 'body'.
        * headers: a mapping of header names to values.
        * body: raw request payload (bytes or str).

    Returns
    -------
    dict
        The decoded JSON body.

    Raises
    ------
    ValueError
        If the content type is not application/json (or a compatible variant).
        If the body cannot be decoded as valid JSON.
    """
    # 1. Validate presence of headers and body
    if not isinstance(req_data, dict):
        raise ValueError("Request data must be a dictionary.")
    headers = req_data.get("headers")
    body = req_data.get("body")

    if headers is None or not isinstance(headers, dict):
        raise ValueError("Missing or invalid 'headers' in request data.")
    if body is None:
        raise ValueError("Missing 'body' in request data.")

    # 2. Check content type
    content_type = headers.get("Content-Type") or headers.get("content-type")
    if not content_type:
        raise ValueError("Content-Type header is missing.")
    # Accept only application/json or related types
    if not content_type.lower().startswith("application/json"):
        raise ValueError(
            f"Unsupported Content-Type: {content_type}. "
            "Only 'application/json' is allowed."
        )

    # 3. Decode body (bytes -> str)
    if isinstance(body, bytes):
        try:
            body_text = body.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise ValueError("Body contains invalid UTF‑8 bytes.") from exc
    elif isinstance(body, str):
        body_text = body
    else:
        raise ValueError("Body must be bytes or str.")

    # 4. Limit body size to mitigate DoS (e.g., 1MB)
    MAX_BODY_SIZE = 1 * 1024 * 1024
    if len(body_text) > MAX_BODY_SIZE:
        raise ValueError("Body exceeds maximum allowed size (1 MB).")

    # 5. Parse JSON
    try:
        parsed = json.loads(body_text)
    except json.JSONDecodeError as exc:
        raise ValueError(f"Invalid JSON: {exc.msg}") from exc

    if not isinstance(parsed, dict):
        raise ValueError("JSON body must be an object (dictionary).")

    return parsed