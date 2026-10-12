import json
from typing import Any, Dict


def validate_json_request(input_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Parse and validate the body of an incoming JSON request.

    Parameters
    ----------
    input_data : dict
        Dictionary containing the request headers and body.
        Expected keys:
            * 'headers' : dict   - HTTP request headers
            * 'body'    : bytes or str  - raw request body

    Returns
    -------
    dict
        The parsed JSON payload.

    Raises
    ------
    ValueError
        If the content type is not application/json.
        If the body cannot be decoded as JSON or if it does not represent a dict.
    """
    # ---- 1. Retrieve headers and body ------------------------------------
    headers = input_data.get("headers", {})
    if not isinstance(headers, dict):
        raise ValueError("Headers must be a dictionary.")

    body = input_data.get("body")
    if body is None:
        raise ValueError("Missing request body.")

    # ---- 2. Validate Content-Type ----------------------------------------
    content_type = headers.get("content-type") or headers.get("Content-Type")
    if not isinstance(content_type, str):
        raise ValueError("Missing or invalid Content-Type header.")

    # Accept only application/json (case‑insensitive, allow charset)
    if not content_type.lower().startswith("application/json"):
        raise ValueError(
            f"Unsupported Content-Type '{content_type}'. Expected 'application/json'."
        )

    # ---- 3. Decode body ----------------------------------------------------
    if isinstance(body, bytes):
        try:
            body_str = body.decode("utf-8")
        except Exception as exc:  # pragma: no cover
            raise ValueError(f"Failed to decode request body as UTF-8: {exc}") from exc
    elif isinstance(body, str):
        body_str = body
    else:  # pragma: no cover
        raise ValueError("Request body must be bytes or str.")

    # Limit size to avoid DoS (CWE-693: protection mechanism failure)
    MAX_BODY_SIZE = 10 * 1024 * 1024  # 10 MB
    if len(body_str) > MAX_BODY_SIZE:
        raise ValueError("Request body too large (exceeds 10 MB).")

    # ---- 4. Parse JSON ----------------------------------------------------
    try:
        parsed = json.loads(body_str)
    except json.JSONDecodeError as exc:  # pragma: no cover
        raise ValueError(f"Invalid JSON payload: {exc}") from exc

    if not isinstance(parsed, dict):
        raise ValueError("JSON payload must be an object (dict).")

    return parsed