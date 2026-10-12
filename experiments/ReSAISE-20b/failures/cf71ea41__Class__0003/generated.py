import json
from typing import Dict, Any

# Maximum allowed body size (bytes) to mitigate denial‑of‑service attacks
MAX_BODY_SIZE = 2 * 1024 * 1024  # 2 MB


def process_json_payload(req_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Parse and validate a JSON request payload.

    Parameters
    ----------
    req_data : dict
        Dictionary containing the HTTP request headers and body. Expected keys:
            - "headers": dict of request headers
            - "body": str or bytes representing the raw body

    Returns
    -------
    dict
        The parsed JSON payload.

    Raises
    ------
    ValueError
        If the Content‑Type header is missing or not a JSON type.
        If the body exceeds ``MAX_BODY_SIZE``.
        If the body is not valid JSON.
    """
    # 1. Validate headers
    headers = req_data.get("headers")
    if not isinstance(headers, dict):
        raise ValueError("Request headers must be a dictionary.")

    content_type = headers.get("Content-Type") or headers.get("content-type")
    if not content_type:
        raise ValueError("Missing Content-Type header.")

    # Accept common JSON MIME types
    json_mime_types = {"application/json", "application/ld+json", "application/vnd.api+json"}
    if not any(content_type.lower().startswith(mime) for mime in json_mime_types):
        raise ValueError(f"Unsupported Content-Type '{content_type}'. Expected JSON.")

    # 2. Retrieve body
    raw_body = req_data.get("body")
    if raw_body is None:
        raise ValueError("Request body is missing.")

    # 3. Ensure body size does not exceed limit
    if isinstance(raw_body, bytes):
        body_bytes = raw_body
    elif isinstance(raw_body, str):
        body_bytes = raw_body.encode("utf-8")
    else:
        raise ValueError("Body must be a string or bytes.")

    if len(body_bytes) > MAX_BODY_SIZE:
        raise ValueError("Request body exceeds maximum allowed size.")

    # 4. Parse JSON safely
    try:
        decoded = body_bytes.decode("utf-8")
        payload = json.loads(decoded)
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ValueError("Malformed JSON payload.") from exc

    if not isinstance(payload, dict):
        raise ValueError("JSON root must be an object (dictionary).")

    return payload