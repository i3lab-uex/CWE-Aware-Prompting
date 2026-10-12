import json
from typing import Dict, Any

def validate_json_request(input_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Parse and validate a JSON request body.

    Parameters
    ----------
    input_data : dict
        Dictionary containing the HTTP headers under the key 'headers'
        and the raw body string under the key 'body'.

    Returns
    -------
    dict
        The parsed JSON payload.

    Raises
    ------
    ValueError
        If the Content-Type header is missing or not JSON.
        If the body cannot be decoded as valid JSON.
    """
    # Extract headers and body safely
    headers = input_data.get("headers", {})
    raw_body = input_data.get("body")

    if raw_body is None:
        raise ValueError("Missing request body.")

    # Normalize header keys to lowercase for case-insensitive lookup
    content_type = None
    for key, value in headers.items():
        if key.lower() == "content-type":
            content_type = value
            break

    # Verify that the request claims to be JSON
    if not content_type or "application/json" not in content_type.lower():
        raise ValueError(
            f"Unsupported Content-Type: {content_type!r}. Expected application/json."
        )

    # Attempt to decode the JSON payload
    try:
        parsed = json.loads(raw_body)
    except json.JSONDecodeError as exc:
        # Provide a clear error message without leaking internal details
        raise ValueError(f"Invalid JSON payload: {exc.msg}") from None

    # Ensure the parsed value is a dictionary (typical for FastAPI models)
    if not isinstance(parsed, dict):
        raise ValueError(
            f"JSON payload must be an object/dictionary, got {type(parsed).__name__}."
        )

    return parsed