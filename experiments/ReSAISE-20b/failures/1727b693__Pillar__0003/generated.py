import json
from typing import Dict, Any

def validate_json_request(input_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Parse and validate the body of an incoming JSON request.

    Parameters
    ----------
    input_data : dict
        Dictionary containing at least the keys:
            - 'headers': mapping of header names to values.
            - 'body'   : raw request body as `str` or `bytes`.

    Returns
    -------
    dict
        The parsed JSON payload.

    Raises
    ------
    ValueError
        If the request is missing required keys, if the Content-Type header does not
        indicate JSON, or if the body cannot be decoded as valid JSON.
    """
    # Ensure required keys exist
    if not isinstance(input_data, dict):
        raise ValueError("Input data must be a dictionary.")
    if 'headers' not in input_data or 'body' not in input_data:
        raise ValueError("Input data must contain 'headers' and 'body' keys.")

    headers = input_data['headers']
    body   = input_data['body']

    # Validate that headers is a dict
    if not isinstance(headers, dict):
        raise ValueError("'headers' must be a dictionary.")

    # Retrieve Content-Type header (case‑insensitive)
    content_type = None
    for key, value in headers.items():
        if key.lower() == 'content-type':
            content_type = value
            break

    # Ensure JSON content type is present
    if not content_type or 'application/json' not in content_type.lower():
        raise ValueError("Unsupported Content-Type. Expected application/json.")

    # Convert body to string if it is bytes
    if isinstance(body, bytes):
        try:
            body_str = body.decode('utf-8')
        except Exception as exc:  # pragma: no cover
            raise ValueError("Failed to decode body bytes.") from exc
    elif isinstance(body, str):
        body_str = body
    else:
        raise ValueError("'body' must be a string or bytes object.")

    # Parse JSON safely
    try:
        parsed = json.loads(body_str)
    except json.JSONDecodeError as exc:  # pragma: no cover
        raise ValueError(f"Invalid JSON payload: {exc.msg}") from exc

    # Ensure the parsed data is a dictionary
    if not isinstance(parsed, dict):
        raise ValueError("JSON payload must be an object (dictionary).")

    return parsed