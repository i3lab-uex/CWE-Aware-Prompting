import json
from typing import Any, Dict

def analyze_json_request(incoming_request: Dict[str, Any]) -> Dict[str, Any]:
    """
    Parse a JSON request body from a FastAPI-like incoming request dictionary.

    Parameters
    ----------
    incoming_request : dict
        A dictionary containing at least the keys 'headers' and 'body'.
        * `headers` should be a dict of HTTP headers.
        * `body` should be the raw request payload (bytes or str).

    Returns
    -------
    dict
        The decoded JSON object.

    Raises
    ------
    ValueError
        If the Content-Type header is not 'application/json' (or a variant).
        If JSON decoding fails due to malformed content.
    """
    # Validate headers
    headers = incoming_request.get("headers", {})
    if not isinstance(headers, dict):
        raise ValueError("Request headers must be a dictionary.")

    content_type = headers.get("Content-Type") or headers.get("content-type")
    if not content_type:
        raise ValueError("Missing Content-Type header.")
    # Allow standard JSON MIME types
    if "application/json" not in content_type.lower():
        raise ValueError(
            f"Unsupported Content-Type: {content_type}. Expected 'application/json'."
        )

    # Get body
    raw_body = incoming_request.get("body")
    if raw_body is None:
        raise ValueError("Missing request body.")
    # Body may be bytes or str; convert to string if needed
    if isinstance(raw_body, bytes):
        try:
            raw_body = raw_body.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise ValueError("Request body is not valid UTF-8.") from exc
    elif not isinstance(raw_body, str):
        raise ValueError("Request body must be a string or bytes.")

    # Decode JSON safely
    try:
        parsed = json.loads(raw_body)
    except json.JSONDecodeError as exc:
        raise ValueError(f"Malformed JSON: {exc.msg}") from exc

    if not isinstance(parsed, dict):
        raise ValueError("JSON payload must be an object (dict).")

    return parsed