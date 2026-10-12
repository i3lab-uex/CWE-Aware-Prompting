import json
from typing import Any, Dict


def analyze_json_request(incoming_request: Dict[str, Any]) -> Dict[str, Any]:
    """
    Parse the JSON body of an incoming FastAPI request.

    Parameters
    ----------
    incoming_request : dict
        A dictionary containing the HTTP headers and body of the request.
        Expected keys:
            - "headers": a dict-like object mapping header names to values
            - "body"   : the raw request body (bytes or str)

    Returns
    -------
    dict
        The decoded JSON object.

    Raises
    ------
    ValueError
        If the Content-Type header is missing or not set to application/json.
        If the body cannot be decoded as valid JSON.
    """
    # Extract headers and body
    headers = incoming_request.get("headers", {})
    if not isinstance(headers, dict):
        raise ValueError("Headers must be a dictionary")

    # Case-insensitive lookup for Content-Type
    content_type = None
    for key, value in headers.items():
        if key.lower() == "content-type":
            content_type = value
            break

    if content_type is None:
        raise ValueError("Missing Content-Type header")

    # Ensure the media type is application/json
    if not content_type.lower().startswith("application/json"):
        raise ValueError(
            f"Unsupported Content-Type '{content_type}'. Expected 'application/json'"
        )

    # Retrieve body
    body = incoming_request.get("body")
    if body is None:
        raise ValueError("Missing request body")

    # Convert bytes to str if necessary
    if isinstance(body, bytes):
        try:
            body_str = body.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise ValueError("Request body is not valid UTF-8") from exc
    elif isinstance(body, str):
        body_str = body
    else:
        raise ValueError("Request body must be bytes or str")

    # Parse JSON
    try:
        parsed = json.loads(body_str)
    except json.JSONDecodeError as exc:
        raise ValueError(f"Malformed JSON: {exc.msg}") from exc

    if not isinstance(parsed, dict):
        raise ValueError("JSON payload must be an object (dictionary)")

    return parsed