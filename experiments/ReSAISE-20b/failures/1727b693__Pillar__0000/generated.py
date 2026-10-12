import json
from typing import Any, Dict


def validate_json_request(input_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Validate and parse the body of an incoming JSON request.

    Parameters
    ----------
    input_data : dict
        Dictionary containing at least two keys:
            - 'headers': a mapping of request headers.
            - 'body'   : the raw request body (bytes or str).

    Returns
    -------
    dict
        The parsed JSON payload.

    Raises
    ------
    ValueError
        If the Content-Type header is missing or not an accepted JSON type.
        If the body cannot be decoded as valid JSON.
    """
    # Extract headers and body
    headers = input_data.get("headers", {})
    raw_body = input_data.get("body")

    if headers is None or not isinstance(headers, dict):
        raise ValueError("Request headers are missing or malformed.")

    # Validate Content-Type header
    content_type = headers.get("Content-Type") or headers.get("content-type")
    if not isinstance(content_type, str) or "application/json" not in content_type.lower():
        raise ValueError("Unsupported Content-Type. Expected application/json.")

    # Ensure body is a string
    if raw_body is None:
        raise ValueError("Request body is missing.")
    if isinstance(raw_body, bytes):
        try:
            raw_body = raw_body.decode("utf-8")
        except Exception as exc:  # pragma: no cover
            raise ValueError("Unable to decode request body as UTF-8.") from exc

    if not isinstance(raw_body, str):
        raise ValueError("Request body must be a string or bytes.")

    # Parse JSON
    try:
        parsed_body = json.loads(raw_body)
    except json.JSONDecodeError as exc:  # pragma: no cover
        raise ValueError(f"Invalid JSON payload: {exc.msg}") from exc

    if not isinstance(parsed_body, dict):
        raise ValueError("JSON payload must be an object (dict).")

    return parsed_body