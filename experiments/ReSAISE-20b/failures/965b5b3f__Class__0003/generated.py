import json
from typing import Dict, Any

def process_json_request(req_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Parse and validate the body of an incoming JSON request.

    Parameters
    ----------
    req_data : dict
        A dictionary containing at least two keys:
            - 'headers'  : mapping of request headers (case‑insensitive)
            - 'body'     : raw body payload (str or bytes)

    Returns
    -------
    dict
        The decoded JSON payload.

    Raises
    ------
    ValueError
        If the Content‑Type header is missing or not `application/json`
        (or a compatible subtype), or if the body cannot be decoded as JSON.
    """
    # Ensure required keys exist
    headers = req_data.get("headers")
    body = req_data.get("body")

    if not isinstance(headers, dict):
        raise ValueError("Request headers must be a dictionary.")
    if body is None:
        raise ValueError("Missing request body.")

    # Normalise header names to lowercase for case‑insensitive lookup
    content_type = None
    for key, value in headers.items():
        if key.lower() == "content-type":
            content_type = str(value).lower()
            break

    if not content_type:
        raise ValueError("Missing Content-Type header.")

    # Accept only application/json or compatible types
    if not content_type.startswith("application/json"):
        raise ValueError(f"Unsupported Content-Type: {content_type}")

    # Convert body to string if it's bytes
    if isinstance(body, bytes):
        try:
            body_str = body.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise ValueError("Body bytes could not be decoded using UTF‑8.") from exc
    elif isinstance(body, str):
        body_str = body
    else:
        raise ValueError("Request body must be a string or bytes object.")

    # Parse JSON safely
    try:
        parsed = json.loads(body_str)
    except json.JSONDecodeError as exc:
        raise ValueError("Invalid JSON payload.") from exc

    if not isinstance(parsed, dict):
        # For stricter validation we could allow other JSON types
        raise ValueError("JSON payload must be an object (dict).")

    return parsed