import json
from typing import Dict, Any


def process_json_request(req_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Parse and validate the body of an incoming JSON request.

    Parameters
    ----------
    req_data : dict
        Dictionary containing the HTTP request headers and body.
        Expected keys are 'headers' (a dict of header names to values)
        and 'body' (the raw request body, bytes or str).

    Returns
    -------
    dict
        The decoded JSON payload.

    Raises
    ------
    ValueError
        If the Content-Type header does not indicate JSON.
        If the body cannot be decoded as valid JSON.
    """
    # 1. Retrieve headers and body
    headers = req_data.get("headers", {})
    raw_body = req_data.get("body")

    # 2. Validate Content-Type
    content_type = headers.get("Content-Type") or headers.get("content-type")
    if not content_type:
        raise ValueError("Missing 'Content-Type' header.")
    # Accept only application/json, optionally with charset
    if not content_type.lower().startswith("application/json"):
        raise ValueError(f"Unsupported Content-Type: {content_type!r}. Expected 'application/json'.")

    # 3. Ensure body is bytes or str
    if raw_body is None:
        raise ValueError("Request body is missing.")
    if isinstance(raw_body, bytes):
        try:
            raw_body = raw_body.decode("utf-8")
        except Exception as exc:  # pragma: no cover
            raise ValueError("Failed to decode request body from bytes.") from exc

    if not isinstance(raw_body, str):
        raise ValueError(f"Request body must be bytes or str, got {type(raw_body).__name__}.")

    # 4. Parse JSON
    try:
        payload = json.loads(raw_body)
    except json.JSONDecodeError as exc:  # pragma: no cover
        raise ValueError(f"Invalid JSON payload: {exc.msg}") from exc

    # 5. Ensure the payload is a dict
    if not isinstance(payload, dict):
        raise ValueError(f"JSON payload must be an object (dict), got {type(payload).__name__}.")

    return payload