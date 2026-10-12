import json
from typing import Dict, Any

# Maximum allowed size for the request body (in bytes) to mitigate DoS attacks
MAX_BODY_SIZE = 1 * 1024 * 1024  # 1 MiB


def decode_json_request(req: Dict[str, Any]) -> Dict[str, Any]:
    """
    Parse and validate a JSON request body from a FastAPI-like dictionary.

    Parameters
    ----------
    req : dict
        Dictionary representing the request, expected to contain:
            - 'headers': a mapping of header names to values (case-insensitive)
            - 'body'   : the raw request body as bytes or str

    Returns
    -------
    dict
        The decoded JSON object.

    Raises
    ------
    ValueError
        If the Content-Type is not 'application/json' (or a compatible subtype)
        or if JSON decoding fails.
    """
    # Ensure headers and body exist
    if 'headers' not in req or 'body' not in req:
        raise ValueError("Missing required request components: headers and body")

    # Normalize header keys to lower case for case‑insensitive lookup
    headers = {k.lower(): v for k, v in req['headers'].items()}

    content_type = headers.get('content-type')
    if not content_type:
        raise ValueError("Missing Content-Type header")

    # Accept only application/json or compatible MIME types
    if not content_type.lower().startswith('application/json'):
        raise ValueError(
            f"Unsupported Content-Type '{content_type}'. Expected 'application/json'"
        )

    body = req['body']

    # Ensure the body is bytes; if it's a string, encode it
    if isinstance(body, str):
        body_bytes = body.encode('utf-8')
    elif isinstance(body, bytes):
        body_bytes = body
    else:
        raise ValueError("Request body must be of type str or bytes")

    # Protect against excessively large payloads
    if len(body_bytes) > MAX_BODY_SIZE:
        raise ValueError("Request body too large")

    try:
        decoded = json.loads(body_bytes.decode('utf-8'))
    except json.JSONDecodeError as exc:
        raise ValueError(f"Invalid JSON payload: {exc.msg}") from exc

    if not isinstance(decoded, dict):
        raise ValueError("JSON payload must be an object (dictionary)")

    return decoded