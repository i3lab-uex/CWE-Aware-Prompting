import json
from typing import Dict, Any

def process_json_request(req_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Parse and validate the body of an incoming JSON request.

    Parameters
    ----------
    req_data : dict
        Dictionary containing the request headers and body.
        Expected keys:
            - "headers": dict of HTTP header names to values
            - "body": bytes or str containing the raw request body

    Returns
    -------
    dict
        Parsed JSON object.

    Raises
    ------
    ValueError
        If the Content-Type header is not application/json (or a compatible type).
        If the body cannot be decoded as valid JSON.
    """
    # 1. Retrieve headers and ensure they are a mapping
    headers = req_data.get("headers")
    if not isinstance(headers, dict):
        raise ValueError("Request headers must be a dictionary.")

    # 2. Verify Content-Type header
    content_type = headers.get("Content-Type") or headers.get("content-type")
    if not isinstance(content_type, str):
        raise ValueError("Content-Type header is missing or invalid.")
    # Allow common JSON MIME types
    if not content_type.lower().startswith("application/json"):
        raise ValueError(
            f"Unsupported Content-Type: {content_type}. Expected application/json."
        )

    # 3. Retrieve body
    body = req_data.get("body")
    if body is None:
        raise ValueError("Request body is missing.")

    # 4. Decode bytes to str if necessary
    if isinstance(body, bytes):
        try:
            body_str = body.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise ValueError("Request body is not valid UTF-8.") from exc
    elif isinstance(body, str):
        body_str = body
    else:
        raise ValueError("Request body must be bytes or str.")

    # 5. Parse JSON safely
    try:
        parsed = json.loads(body_str)
    except json.JSONDecodeError as exc:
        raise ValueError("Request body contains invalid JSON.") from exc

    # 6. Ensure the parsed value is a dictionary (JSON object)
    if not isinstance(parsed, dict):
        raise ValueError("Request JSON must be an object (dict).")

    return parsed