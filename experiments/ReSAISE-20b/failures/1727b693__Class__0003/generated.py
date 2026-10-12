import json
from typing import Dict, Any


def validate_json_request(input_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Parse and validate the body of an incoming JSON request.

    Parameters
    ----------
    input_data : dict
        Dictionary containing at least two keys:
            * ``headers``: Mapping of request headers.
            * ``body``   : Raw body content (bytes or str).

    Returns
    -------
    dict
        The parsed JSON payload.

    Raises
    ------
    ValueError
        If the ``Content-Type`` header is missing or not an accepted JSON media type,
        or if the body cannot be decoded as valid JSON.
    """
    # Validate presence of headers and body
    if not isinstance(input_data, dict):
        raise ValueError("Input data must be a dictionary.")
    headers = input_data.get("headers")
    body = input_data.get("body")

    if headers is None or not isinstance(headers, dict):
        raise ValueError("Missing or invalid 'headers' in input data.")
    if body is None:
        raise ValueError("Missing 'body' in input data.")

    # Normalize header keys to lower case for robust matching
    content_type = headers.get("Content-Type") or headers.get("content-type")
    if not content_type:
        raise ValueError("Missing 'Content-Type' header.")

    # Accept only JSON media types (including optional charset)
    if not content_type.lower().startswith("application/json"):
        raise ValueError(
            f"Unsupported Content-Type '{content_type}'. Expected 'application/json'."
        )

    # Decode body if it is bytes
    if isinstance(body, bytes):
        try:
            body_text = body.decode("utf-8")
        except Exception as exc:
            raise ValueError(f"Body bytes could not be decoded: {exc}") from exc
    elif isinstance(body, str):
        body_text = body
    else:
        raise ValueError("Body must be a string or bytes object.")

    # Parse JSON
    try:
        payload = json.loads(body_text)
    except json.JSONDecodeError as exc:
        raise ValueError(f"Invalid JSON payload: {exc}") from exc

    if not isinstance(payload, dict):
        raise ValueError("JSON payload must be an object (dictionary).")

    return payload