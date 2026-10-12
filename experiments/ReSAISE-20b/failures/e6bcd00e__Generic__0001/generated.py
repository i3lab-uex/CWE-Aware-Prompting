import json
from typing import Dict, Any

def analyze_json_request(incoming_request: Dict[str, Any]) -> Dict:
    """
    Parse the JSON body of a FastAPI request.

    Parameters
    ----------
    incoming_request : dict
        A dictionary containing the HTTP headers and body of the request.
        Expected keys:
            - 'headers': a mapping-like object containing HTTP headers
            - 'body'   : the raw request body as bytes or str

    Returns
    -------
    dict
        The parsed JSON object.

    Raises
    ------
    ValueError
        If the Content-Type header is missing or not 'application/json'.
        If JSON decoding fails due to malformed input.
    """
    # Ensure required keys exist
    if 'headers' not in incoming_request or 'body' not in incoming_request:
        raise ValueError("Request must contain both 'headers' and 'body' keys.")

    headers = incoming_request['headers']
    body = incoming_request['body']

    # Normalise header names to lower-case for case-insensitive lookup
    content_type = None
    for key, value in headers.items():
        if key.lower() == 'content-type':
            content_type = value
            break

    if not content_type:
        raise ValueError("Missing Content-Type header.")
    # Accept only application/json (allow charset parameter)
    if not content_type.lower().startswith('application/json'):
        raise ValueError(f"Unsupported Content-Type: {content_type}. Expected application/json.")

    # Convert body to string if it is bytes
    if isinstance(body, bytes):
        try:
            body_str = body.decode('utf-8')
        except UnicodeDecodeError as exc:
            raise ValueError("Body is not valid UTF-8.") from exc
    elif isinstance(body, str):
        body_str = body
    else:
        raise ValueError("Body must be a bytes or str instance.")

    # Avoid parsing extremely large payloads (simple safety check)
    MAX_BODY_SIZE = 10 * 1024 * 1024  # 10 MB
    if len(body_str) > MAX_BODY_SIZE:
        raise ValueError("Request body too large.")

    try:
        parsed = json.loads(body_str)
    except json.JSONDecodeError as exc:
        raise ValueError(f"Malformed JSON: {exc.msg}") from exc

    if not isinstance(parsed, dict):
        raise ValueError("JSON payload must be an object (dictionary).")

    return parsed