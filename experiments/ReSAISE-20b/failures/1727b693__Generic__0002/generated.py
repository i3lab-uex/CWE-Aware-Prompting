import json
from typing import Any, Dict


def validate_json_request(input_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Parse and validate the body of an incoming JSON request.

    Parameters
    ----------
    input_data : dict
        Dictionary containing at least two keys:
            - "headers": mapping of request headers (case-insensitive)
            - "body": raw body data as bytes or str

    Returns
    -------
    dict
        Parsed JSON object.

    Raises
    ------
    ValueError
        If the content type is not acceptable or JSON decoding fails.
    """
    # Retrieve headers and body
    headers = input_data.get("headers", {})
    body = input_data.get("body")

    if not isinstance(headers, dict):
        raise ValueError("Headers must be a dictionary.")

    # Normalise header keys to lowercase for case-insensitive lookup
    headers_normalised = {k.lower(): v for k, v in headers.items()}

    content_type = headers_normalised.get("content-type", "")
    if "application/json" not in content_type.lower():
        raise ValueError("Unsupported Content-Type. Expected application/json.")

    if body is None:
        raise ValueError("Request body is missing.")

    # Ensure body is a string before parsing
    if isinstance(body, bytes):
        try:
            body_str = body.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise ValueError(f"Body decoding error: {exc}") from exc
    elif isinstance(body, str):
        body_str = body
    else:
        raise ValueError("Body must be a string or bytes.")

    try:
        parsed = json.loads(body_str)
    except json.JSONDecodeError as exc:
        raise ValueError(f"Invalid JSON: {exc}") from exc

    if not isinstance(parsed, dict):
        raise ValueError("JSON payload must be an object (dict).")

    return parsed