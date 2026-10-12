import json
from typing import Any, Dict


def analyze_json_request(incoming_request: Dict[str, Any]) -> Dict[str, Any]:
    """
    Parse a JSON request body from an incoming FastAPI request.

    Parameters
    ----------
    incoming_request : dict
        Dictionary containing the HTTP headers and body of the request.
        Expected keys:
            - "headers" : dict[str, str]
            - "body"    : str | bytes

    Returns
    -------
    dict
        The parsed JSON body.

    Raises
    ------
    ValueError
        If the Content-Type header is missing or not `application/json`.
        If the body cannot be decoded as JSON.
    """
    # Extract headers and body
    headers = incoming_request.get("headers", {})
    if not isinstance(headers, dict):
        raise ValueError("Headers must be a dictionary.")

    # Verify Content-Type
    content_type = headers.get("Content-Type") or headers.get("content-type")
    if not content_type:
        raise ValueError("Missing 'Content-Type' header.")
    # Normalise and compare
    if content_type.lower().split(";")[0].strip() != "application/json":
        raise ValueError(
            f"Unsupported Content-Type '{content_type}'. "
            "Only 'application/json' is accepted."
        )

    # Retrieve body
    body = incoming_request.get("body")
    if body is None:
        raise ValueError("Missing request body.")
    # Body may be bytes; convert to str if needed
    if isinstance(body, bytes):
        try:
            body = body.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise ValueError("Request body is not valid UTF-8.") from exc
    elif not isinstance(body, str):
        raise ValueError("Request body must be a string or bytes.")

    # Parse JSON
    try:
        parsed = json.loads(body)
    except json.JSONDecodeError as exc:
        raise ValueError(f"Malformed JSON: {exc.msg}") from exc

    if not isinstance(parsed, dict):
        raise ValueError("JSON payload must be an object (dictionary).")

    return parsed