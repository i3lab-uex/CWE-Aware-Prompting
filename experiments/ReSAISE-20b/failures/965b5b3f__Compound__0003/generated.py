import json
from typing import Dict, Any

def process_json_request(req_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Parse and validate the body of an incoming JSON request.

    Parameters
    ----------
    req_data : dict
        Dictionary containing at least the following keys:
            - "headers": a mapping of request headers (case-insensitive)
            - "body": the raw request body as bytes or string

    Returns
    -------
    dict
        The decoded JSON payload.

    Raises
    ------
    ValueError
        If the request content type is not `application/json` (or a subtype of it).
    ValueError
        If the body cannot be decoded as valid JSON.
    """
    # Extract headers and body from the request data
    headers = req_data.get("headers", {})
    raw_body = req_data.get("body")

    # Normalise header names to lower case for case‑insensitive lookup
    headers_lower = {k.lower(): v for k, v in headers.items()}

    # Verify that the Content‑Type header is present and acceptable
    content_type = headers_lower.get("content-type")
    if not content_type:
        raise ValueError("Missing 'Content-Type' header in request.")

    # Accept only application/json and its subtypes (e.g., application/vnd.api+json)
    if not content_type.lower().startswith("application/json"):
        raise ValueError(
            f"Unsupported Content-Type '{content_type}'. "
            "Only 'application/json' is accepted."
        )

    # Convert the raw body to a string if it is bytes
    if isinstance(raw_body, bytes):
        try:
            raw_body = raw_body.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise ValueError("Request body is not valid UTF‑8.") from exc

    if not isinstance(raw_body, str):
        raise ValueError("Request body must be a string or bytes.")

    # Parse the JSON payload
    try:
        parsed_body = json.loads(raw_body)
    except json.JSONDecodeError as exc:
        raise ValueError(f"Invalid JSON payload: {exc.msg}") from exc

    # The parsed body must be a dictionary for FastAPI Pydantic models
    if not isinstance(parsed_body, dict):
        raise ValueError("JSON payload must be an object (dictionary).")

    return parsed_body