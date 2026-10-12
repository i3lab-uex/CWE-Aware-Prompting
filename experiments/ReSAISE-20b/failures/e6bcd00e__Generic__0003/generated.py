import json
from typing import Dict, Any


def analyze_json_request(incoming_request: Dict[str, Any]) -> Dict[str, Any]:
    """
    Parse the JSON body of a FastAPI request.

    Parameters
    ----------
    incoming_request : dict
        Dictionary containing HTTP headers under the key 'headers'
        and the raw request body string under the key 'body'.

    Returns
    -------
    dict
        Parsed JSON object.

    Raises
    ------
    ValueError
        If the `Content-Type` header is missing or not JSON, or if the body
        cannot be decoded as valid JSON.
    """
    # Retrieve headers and body from the request dict
    headers = incoming_request.get("headers", {})
    raw_body = incoming_request.get("body")

    if raw_body is None:
        raise ValueError("Request body is missing.")

    # Normalize header names to lowercase for case‑insensitive comparison
    content_type = headers.get("content-type") or headers.get("Content-Type")
    if not content_type:
        raise ValueError("Missing Content-Type header.")

    # Accept common JSON media types
    if "application/json" not in content_type.lower():
        raise ValueError(
            f"Unsupported Content-Type '{content_type}'. Expected 'application/json'."
        )

    # Prevent processing extremely large bodies (e.g., > 10 MB)
    MAX_BODY_SIZE = 10 * 1024 * 1024
    if isinstance(raw_body, str) and len(raw_body.encode("utf-8")) > MAX_BODY_SIZE:
        raise ValueError("Request body exceeds maximum allowed size.")

    # Attempt to parse the JSON payload
    try:
        parsed = json.loads(raw_body)
    except json.JSONDecodeError as exc:
        raise ValueError(f"Malformed JSON: {exc.msg}") from exc

    # Ensure the parsed payload is a dictionary (JSON object)
    if not isinstance(parsed, dict):
        raise ValueError("JSON payload must be an object (dictionary).")

    return parsed