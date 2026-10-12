import json
from typing import Dict, Any


def handle_json_input(client_request: Dict[str, Any]) -> Dict[str, Any]:
    """
    Parse and validate the JSON body of an incoming HTTP request.

    Parameters
    ----------
    client_request : dict
        A dictionary containing at least the keys 'headers' and 'body'.
        ``client_request['headers']`` should be a mapping of header names
        to values (case‑insensitive). ``client_request['body']`` can be a
        string or bytes representing the raw request payload.

    Returns
    -------
    dict
        The parsed JSON body as a Python dictionary.

    Raises
    ------
    ValueError
        If the request does not declare a JSON content type or if the body
        cannot be decoded as valid JSON.
    """
    # Ensure required keys are present
    if 'headers' not in client_request or 'body' not in client_request:
        raise ValueError("Request must contain both 'headers' and 'body'")

    headers = client_request['headers']
    body = client_request['body']

    # Normalise header names to lowercase for case‑insensitive lookup
    headers_lower = {k.lower(): v for k, v in headers.items()}

    content_type = headers_lower.get('content-type', '')
    if not any(ct in content_type.lower() for ct in ('application/json',
                                                    'application/ld+json',
                                                    'application/vnd.api+json')):
        raise ValueError("Content-Type must be a JSON-compatible type")

    # Decode body if it's bytes
    if isinstance(body, bytes):
        try:
            body_str = body.decode('utf-8')
        except UnicodeDecodeError as exc:
            raise ValueError("Request body is not valid UTF‑8") from exc
    elif isinstance(body, str):
        body_str = body
    else:
        raise ValueError("Request body must be a string or bytes")

    # Parse JSON
    try:
        parsed = json.loads(body_str)
    except json.JSONDecodeError as exc:
        raise ValueError("Malformed JSON in request body") from exc

    if not isinstance(parsed, dict):
        raise ValueError("JSON root must be an object")

    return parsed