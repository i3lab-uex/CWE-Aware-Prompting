import json
from typing import Dict, Any

# Maximum allowed size for a JSON body (bytes). Adjust as needed.
MAX_BODY_SIZE = 10 * 1024 * 1024  # 10 MB

def decode_json_request(req: Dict[str, Any]) -> Dict[str, Any]:
    """
    Parse and validate the body of an incoming JSON request.

    Parameters
    ----------
    req : dict
        Dictionary containing at least the keys 'headers' and 'body'.
        - headers: mapping of header names to values (case-insensitive).
        - body: bytes or string representing the raw request payload.

    Returns
    -------
    dict
        The decoded JSON object as a Python dictionary.

    Raises
    ------
    ValueError
        If the request content type is not 'application/json' (or a subtype)
        or if JSON decoding fails.
    """
    # Ensure headers are present and normalized to lower case for case‑insensitive lookup
    if not isinstance(req, dict):
        raise ValueError("Request must be a dictionary with 'headers' and 'body' keys.")

    headers = req.get("headers")
    body = req.get("body")

    if not isinstance(headers, dict):
        raise ValueError("'headers' must be a dictionary.")
    if body is None:
        raise ValueError("Missing request body.")

    # Normalize header names to lower case for consistent lookup
    normalized_headers = {k.lower(): v for k, v in headers.items()}

    content_type = normalized_headers.get("content-type")
    if not content_type or "application/json" not in content_type.lower():
        raise ValueError("Unsupported Content-Type. Expected application/json.")

    # Enforce body size limit to mitigate DoS attacks
    if isinstance(body, (bytes, bytearray)):
        body_bytes = body
    elif isinstance(body, str):
        body_bytes = body.encode("utf-8")
    else:
        raise ValueError("Body must be bytes or string.")

    if len(body_bytes) > MAX_BODY_SIZE:
        raise ValueError(f"Request body too large. Max allowed is {MAX_BODY_SIZE} bytes.")

    try:
        decoded = json.loads(body_bytes.decode("utf-8"))
    except (json.JSONDecodeError, UnicodeDecodeError) as exc:
        raise ValueError(f"Invalid JSON payload: {exc}") from exc

    if not isinstance(decoded, dict):
        raise ValueError("JSON payload must be an object (dictionary).")

    return decoded