import json
from typing import Dict, Any

def handle_json_input(client_request: Dict[str, Any]) -> Dict[Any, Any]:
    """
    Parse and validate a JSON request body.

    Parameters
    ----------
    client_request : dict
        Dictionary containing at least the keys 'headers' and 'body'.
        ``client_request['headers']`` must be a dict-like object
        mapping header names to values.
        ``client_request['body']`` must be a str containing JSON.

    Returns
    -------
    dict
        The decoded JSON object from the request body.

    Raises
    ------
    ValueError
        If the Content-Type header does not indicate JSON.
        If the body is not valid JSON.
    """
    # Ensure required keys exist
    if 'headers' not in client_request or 'body' not in client_request:
        raise ValueError("Request must contain 'headers' and 'body' keys")

    headers = client_request['headers']
    body = client_request['body']

    # Normalize header names to lowercase for case‑insensitive comparison
    content_type = None
    for key, value in headers.items():
        if key.lower() == 'content-type':
            content_type = value
            break

    # Validate that the Content-Type indicates JSON
    if not content_type or 'application/json' not in content_type.lower():
        raise ValueError("Content-Type must be application/json or compatible")

    # Parse the JSON body safely
    try:
        parsed = json.loads(body)
    except (json.JSONDecodeError, TypeError) as exc:
        raise ValueError("Malformed JSON in request body") from exc

    # Ensure the parsed result is a dict (typical for FastAPI models)
    if not isinstance(parsed, dict):
        raise ValueError("JSON body must represent an object (dict)")

    return parsed