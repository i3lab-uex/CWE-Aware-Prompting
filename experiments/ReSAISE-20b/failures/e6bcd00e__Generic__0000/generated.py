import json

def analyze_json_request(incoming_request: dict) -> dict:
    """
    Parse the JSON body of an incoming FastAPI request.

    Parameters
    ----------
    incoming_request : dict
        A dictionary containing both the HTTP headers and body of the request.
        Expected keys:
            - 'headers': a mapping of header names to values
            - 'body'   : the raw request body as a string or bytes

    Returns
    -------
    dict
        The decoded JSON object.

    Raises
    ------
    ValueError
        If the `Content-Type` header is not 'application/json' or if the body cannot be
        decoded as JSON.
    """
    # Retrieve headers and body, normalizing header names to lowercase
    headers = incoming_request.get("headers", {})
    content_type = headers.get("content-type") or headers.get("Content-Type")

    if not content_type or "application/json" not in content_type.lower():
        raise ValueError("Invalid content type: expected 'application/json'")

    body = incoming_request.get("body")
    if body is None:
        raise ValueError("Missing request body")

    # If the body is bytes, decode to string
    if isinstance(body, bytes):
        try:
            body = body.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise ValueError(f"Body is not valid UTF-8: {exc}") from exc

    # Guard against excessively large payloads (optional)
    MAX_BODY_SIZE = 10 * 1024 * 1024  # 10 MB
    if len(body) > MAX_BODY_SIZE:
        raise ValueError("Request body too large")

    try:
        parsed = json.loads(body)
    except json.JSONDecodeError as exc:
        raise ValueError(f"Malformed JSON: {exc}") from exc

    if not isinstance(parsed, dict):
        raise ValueError("JSON payload must be an object (dictionary)")

    return parsed