import json
from typing import Dict, Any

class MalformedRequestError(ValueError):
    """Raised when the request body is not valid JSON."""
    pass

class UnsupportedContentTypeError(ValueError):
    """Raised when the Content-Type header is not JSON-compatible."""
    pass

def handle_json_input(client_request: Dict[str, Any]) -> Dict[str, Any]:
    """
    Parse and validate a JSON request body.

    Parameters
    ----------
    client_request : dict
        Dictionary containing the HTTP request headers and body. Expected keys:
            - "headers": a mapping of header names to values
            - "body": the raw request body (str or bytes)

    Returns
    -------
    dict
        The parsed JSON payload.

    Raises
    ------
    UnsupportedContentTypeError
        If the Content-Type header does not indicate JSON.
    MalformedRequestError
        If the body cannot be parsed as JSON.
    """
    # Ensure required keys exist
    if not isinstance(client_request, dict):
        raise ValueError("client_request must be a dictionary")

    headers = client_request.get("headers")
    body = client_request.get("body")

    if headers is None or body is None:
        raise ValueError("client_request must contain 'headers' and 'body' keys")

    if not isinstance(headers, dict):
        raise ValueError("'headers' must be a dictionary")

    # Normalise header names to lower case for comparison
    content_type = None
    for key, value in headers.items():
        if isinstance(key, str) and key.lower() == "content-type":
            content_type = value
            break

    if not content_type or not isinstance(content_type, str):
        raise UnsupportedContentTypeError("Missing or invalid Content-Type header")

    # Accept common JSON media types
    json_media_types = {"application/json", "application/ld+json", "application/vnd.api+json"}
    if not any(ct.lower().startswith(mt) for mt in json_media_types for ct in [content_type]):
        raise UnsupportedContentTypeError(f"Unsupported Content-Type: {content_type}")

    # Convert body to string if bytes
    if isinstance(body, bytes):
        try:
            body_text = body.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise MalformedRequestError("Body contains invalid UTF-8 bytes") from exc
    elif isinstance(body, str):
        body_text = body
    else:
        raise MalformedRequestError("Body must be a string or bytes")

    # Parse JSON
    try:
        payload = json.loads(body_text)
    except json.JSONDecodeError as exc:
        raise MalformedRequestError(f"Invalid JSON: {exc.msg}") from exc

    if not isinstance(payload, dict):
        raise MalformedRequestError("JSON payload must be an object (dict)")

    return payload