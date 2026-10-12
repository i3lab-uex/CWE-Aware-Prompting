import json
from typing import Any, Dict


def parse_json_request(request: Dict[str, Any]) -> Dict[str, Any]:
    """
    Parse and validate a JSON request body.

    Parameters
    ----------
    request : dict
        A dictionary representing the incoming request. Expected keys are:
        - "headers": a mapping of header names to values
        - "body": the raw request body (bytes or str)

    Returns
    -------
    dict
        The decoded JSON payload as a Python dictionary.

    Raises
    ------
    ValueError
        If the request does not contain a valid JSON body or if the
        Content-Type header is missing/incorrect.
    """
    # Basic request structure validation
    if not isinstance(request, dict):
        raise ValueError("Request must be a dictionary")

    headers = request.get("headers")
    body = request.get("body")

    if not isinstance(headers, dict):
        raise ValueError("Request headers must be a dictionary")
    if body is None:
        raise ValueError("Missing request body")

    # Verify Content-Type header (case-insensitive)
    content_type = headers.get("Content-Type") or headers.get("content-type")
    if not isinstance(content_type, str) or "application/json" not in content_type.lower():
        raise ValueError("Invalid or missing Content-Type header for JSON payload")

    # Ensure body is bytes or str
    if isinstance(body, bytes):
        try:
            body_str = body.decode("utf-8")
        except Exception as exc:
            raise ValueError(f"Failed to decode body bytes: {exc}") from exc
    elif isinstance(body, str):
        body_str = body
    else:
        raise ValueError("Request body must be bytes or str")

    # Parse JSON
    try:
        payload = json.loads(body_str)
    except json.JSONDecodeError as exc:
        raise ValueError(f"JSON decoding failed: {exc}") from exc

    # Ensure the payload is a dictionary
    if not isinstance(payload, dict):
        raise ValueError("JSON payload must be an object (dictionary)")

    return payload