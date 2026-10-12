import json
from typing import Dict, Any


def analyze_json_request(incoming_request: Dict[str, Any]) -> Dict[str, Any]:
    """
    Parse the JSON body of an incoming FastAPI request.

    Parameters
    ----------
    incoming_request : dict
        Dictionary containing the HTTP headers and body of the request.
        Expected keys are 'headers' (a dict) and 'body' (a str or bytes).

    Returns
    -------
    dict
        Parsed JSON object.

    Raises
    ------
    ValueError
        If the Content-Type header is missing or not `application/json`,
        or if JSON decoding fails due to malformed input.
    """
    # Validate presence of headers and body
    if not isinstance(incoming_request, dict):
        raise ValueError("incoming_request must be a dictionary")
    headers = incoming_request.get("headers", {})
    body = incoming_request.get("body")

    if not isinstance(headers, dict):
        raise ValueError("'headers' must be a dictionary")
    if body is None:
        raise ValueError("Request body is missing")

    # Ensure Content-Type is application/json
    content_type = headers.get("Content-Type") or headers.get("content-type")
    if not content_type:
        raise ValueError("Missing Content-Type header")
    # Normalize to lowercase and strip parameters (e.g., charset)
    media_type = content_type.split(";")[0].strip().lower()
    if media_type != "application/json":
        raise ValueError(f"Unsupported Content-Type: {content_type}")

    # Convert body to string if it is bytes
    if isinstance(body, bytes):
        try:
            body_str = body.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise ValueError(f"Body is not valid UTF-8: {exc}") from exc
    elif isinstance(body, str):
        body_str = body
    else:
        raise ValueError("Body must be a string or bytes")

    # Parse JSON
    try:
        parsed = json.loads(body_str)
    except json.JSONDecodeError as exc:
        raise ValueError(f"Malformed JSON: {exc}") from exc

    if not isinstance(parsed, dict):
        raise ValueError("JSON body must be an object (dictionary)")

    return parsed