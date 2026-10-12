import json
from typing import Dict, Any

# Constants for header names and accepted content type
CONTENT_TYPE_HEADER = "Content-Type"
CSRF_TOKEN_HEADER = "X-CSRF-Token"
ACCEPTED_CONTENT_TYPE = "application/json"

def process_json_request(req_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Parse and validate the body of an incoming JSON request.

    Parameters
    ----------
    req_data : dict
        A dictionary that must contain at least the keys ``headers`` and ``body``.
        * headers : dict
            HTTP request headers (case-insensitive keys are acceptable).
        * body : bytes or str
            The raw request payload.

    Returns
    -------
    dict
        The decoded JSON object from the request body.

    Raises
    ------
    ValueError
        If the content type is not application/json,
        if a CSRF token header is missing or empty,
        or if the body cannot be decoded as valid JSON.
    """
    # 1. Extract headers and normalize key names to lower case
    raw_headers = req_data.get("headers", {})
    headers = {k.lower(): v for k, v in raw_headers.items()}

    # 2. Verify content type
    content_type = headers.get(CONTENT_TYPE_HEADER.lower())
    if content_type is None or ACCEPTED_CONTENT_TYPE not in content_type.split(";")[0].strip().lower():
        raise ValueError("Unsupported or missing Content-Type header; application/json required.")

    # 3. Verify CSRF token presence (basic protection)
    csrf_token = headers.get(CSRF_TOKEN_HEADER.lower())
    if not csrf_token:
        raise ValueError("Missing CSRF token header; request may be forged.")

    # 4. Retrieve and decode body
    raw_body = req_data.get("body")
    if raw_body is None:
        raise ValueError("Request body is missing.")

    # Body may be bytes or str
    if isinstance(raw_body, bytes):
        try:
            body_str = raw_body.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise ValueError(f"Body decoding failed: {exc}") from exc
    elif isinstance(raw_body, str):
        body_str = raw_body
    else:
        raise ValueError("Body must be of type bytes or str.")

    # 5. Parse JSON
    try:
        json_body = json.loads(body_str)
    except json.JSONDecodeError as exc:
        raise ValueError(f"Invalid JSON format: {exc}") from exc

    # 6. Return parsed body
    return json_body