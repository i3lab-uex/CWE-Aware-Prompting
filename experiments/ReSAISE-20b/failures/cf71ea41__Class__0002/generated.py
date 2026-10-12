import json
from typing import Dict, Any


def process_json_payload(req_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Validate and parse a JSON request payload.

    Parameters
    ----------
    req_data : dict
        Dictionary that includes both the headers and body of the HTTP request.
        Expected keys are:
            - "headers": a dict containing request headers
            - "body": the raw request body (bytes or str)

    Returns
    -------
    dict
        The parsed JSON payload.

    Raises
    ------
    ValueError
        If the content-type header is not set to a JSON-compatible format.
        If the body cannot be parsed as valid JSON.
    """
    # Extract headers and body
    headers = req_data.get("headers", {})
    body = req_data.get("body")

    # 1. Verify content-type header
    content_type = headers.get("Content-Type") or headers.get("content-type")
    if not content_type:
        raise ValueError("Missing Content-Type header")

    # Accept common JSON MIME types
    json_mime_types = {"application/json", "application/ld+json",
                       "application/vnd.api+json"}
    if not any(content_type.lower().startswith(mime) for mime in json_mime_types):
        raise ValueError(f"Unsupported Content-Type: {content_type}")

    # 2. Decode body to string if it's bytes
    if isinstance(body, bytes):
        try:
            body_str = body.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise ValueError("Body is not valid UTF-8") from exc
    elif isinstance(body, str):
        body_str = body
    else:
        raise ValueError("Body must be a string or bytes")

    # 3. Parse JSON
    try:
        parsed = json.loads(body_str)
    except json.JSONDecodeError as exc:
        raise ValueError("Malformed JSON payload") from exc

    # 4. Ensure the result is a dict (JSON object)
    if not isinstance(parsed, dict):
        raise ValueError("JSON payload must be an object (dict)")

    return parsed