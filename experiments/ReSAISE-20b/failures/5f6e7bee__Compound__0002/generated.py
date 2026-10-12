import json
from typing import Dict, Any


def handle_json_request(http_request: Dict[str, Any]) -> Dict[str, Any]:
    """
    Parse a JSON request body from a FastAPI-style HTTP request dictionary.

    Parameters
    ----------
    http_request : dict
        A dictionary containing the HTTP headers and body of the incoming request.
        Expected keys are:
            - "headers": a dict mapping header names to values
            - "body": the raw request body (bytes or str)

    Returns
    -------
    dict
        The parsed JSON object.

    Raises
    ------
    ValueError
        If the Content-Type header is missing or not 'application/json'.
        If the JSON decoding fails due to malformed input.
    """
    # Validate presence of headers and body
    if not isinstance(http_request, dict):
        raise ValueError("Request must be a dictionary containing 'headers' and 'body'.")
    headers = http_request.get("headers", {})
    body = http_request.get("body")

    if not isinstance(headers, dict):
        raise ValueError("'headers' must be a dictionary.")
    if body is None:
        raise ValueError("Missing request body.")

    # Normalise header names to lower case for comparison
    content_type = headers.get("Content-Type") or headers.get("content-type")
    if not content_type:
        raise ValueError("Missing Content-Type header.")
    if "application/json" not in content_type.lower():
        raise ValueError(
            f"Unsupported Content-Type '{content_type}'. Expected 'application/json'."
        )

    # Ensure body is bytes or string
    if isinstance(body, bytes):
        try:
            body_text = body.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise ValueError(f"Body decoding failed: {exc}") from exc
    elif isinstance(body, str):
        body_text = body
    else:
        raise ValueError("Request body must be bytes or string.")

    # Parse JSON safely
    try:
        parsed = json.loads(body_text)
    except json.JSONDecodeError as exc:
        raise ValueError(f"Malformed JSON: {exc}") from exc

    if not isinstance(parsed, dict):
        raise ValueError("JSON payload must be an object (dictionary).")

    return parsed