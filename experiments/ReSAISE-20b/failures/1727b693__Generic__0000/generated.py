import json
from typing import Dict, Any

# Max body size to guard against large payloads (1 MB)
_MAX_BODY_SIZE = 1024 * 1024  # bytes

def validate_json_request(input_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Validate and parse a JSON request body.

    Parameters
    ----------
    input_data : dict
        Dictionary containing the request headers and body. Expected keys:
            * ``headers`` (dict): Request HTTP headers.
            * ``body`` (bytes or str): Raw request body.

    Returns
    -------
    dict
        The decoded JSON payload as a Python dictionary.

    Raises
    ------
    ValueError
        If the Content-Type header is missing or not a JSON type,
        if the body exceeds the maximum allowed size, or
        if the body cannot be decoded as JSON.
    """
    # ------------------------------------------------------------------
    # 1. Validate presence of required keys
    # ------------------------------------------------------------------
    if not isinstance(input_data, dict):
        raise ValueError("Input data must be a dictionary.")
    headers = input_data.get("headers")
    body = input_data.get("body")

    if headers is None or not isinstance(headers, dict):
        raise ValueError("Missing or invalid 'headers' in input data.")
    if body is None:
        raise ValueError("Missing request body.")

    # ------------------------------------------------------------------
    # 2. Validate Content-Type header
    # ------------------------------------------------------------------
    content_type = headers.get("Content-Type") or headers.get("content-type")
    if not content_type:
        raise ValueError("Missing Content-Type header.")
    # Accept application/json or variants (e.g., application/json; charset=utf-8)
    if not content_type.lower().startswith("application/json"):
        raise ValueError(
            f"Unsupported Content-Type '{content_type}'. "
            "Only 'application/json' is accepted."
        )

    # ------------------------------------------------------------------
    # 3. Size check
    # ------------------------------------------------------------------
    if isinstance(body, bytes):
        body_len = len(body)
    elif isinstance(body, str):
        body_len = len(body.encode("utf-8"))
    else:
        raise ValueError("Request body must be bytes or string.")
    if body_len > _MAX_BODY_SIZE:
        raise ValueError("Request body exceeds maximum allowed size.")

    # ------------------------------------------------------------------
    # 4. Decode JSON
    # ------------------------------------------------------------------
    try:
        if isinstance(body, bytes):
            decoded = json.loads(body.decode("utf-8"))
        else:
            decoded = json.loads(body)
    except json.JSONDecodeError as exc:
        raise ValueError(f"Invalid JSON payload: {exc}") from exc

    if not isinstance(decoded, dict):
        raise ValueError("JSON payload must be an object (dict).")

    return decoded