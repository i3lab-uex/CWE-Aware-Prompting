import json
from typing import Dict, Any

def decode_json_request(req: Dict[str, Any]) -> Dict[str, Any]:
    """
    Parse and validate a JSON request body.

    Parameters
    ----------
    req : dict
        Dictionary containing at least the keys 'headers' and 'body'.
        `headers` should be a mapping of header names to values.
        `body` should be a bytes or str object containing the raw request payload.

    Returns
    -------
    dict
        The decoded JSON object.

    Raises
    ------
    ValueError
        If the Content-Type is not acceptable or if JSON decoding fails.
    """
    # Retrieve headers and body
    headers = req.get("headers", {})
    if not isinstance(headers, dict):
        raise ValueError("Request headers must be a dictionary")

    # Normalise header keys to lower case for case‑insensitive comparison
    content_type = None
    for key, value in headers.items():
        if key.lower() == "content-type":
            content_type = value
            break

    # Verify that the Content-Type is acceptable
    if not content_type or "application/json" not in content_type.lower():
        raise ValueError("Unsupported Content-Type. Expected application/json")

    # Retrieve body
    raw_body = req.get("body")
    if raw_body is None:
        raise ValueError("Missing request body")

    # Ensure the body is a string for json.loads
    if isinstance(raw_body, bytes):
        try:
            raw_body = raw_body.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise ValueError("Request body is not valid UTF‑8") from exc
    elif not isinstance(raw_body, str):
        raise ValueError("Request body must be a string or bytes")

    # Decode JSON
    try:
        decoded = json.loads(raw_body)
    except json.JSONDecodeError as exc:
        raise ValueError(f"Invalid JSON payload: {exc.msg}") from exc

    # Ensure the decoded object is a dictionary
    if not isinstance(decoded, dict):
        raise ValueError("JSON payload must be an object (dictionary)")

    return decoded