import json
from typing import Dict, Any

# Maximum allowed size for the request body (in bytes) to mitigate DoS attacks.
MAX_BODY_SIZE = 10 * 1024 * 1024  # 10 MB


def process_json_input(req: Dict[str, Any]) -> Dict[str, Any]:
    """
    Parse the JSON body of an incoming FastAPI request.

    Parameters
    ----------
    req : dict
        Dictionary containing the HTTP headers and body of the request.
        Expected keys are:
            - "headers": dict mapping header names to values
            - "body": bytes or str containing the raw request body

    Returns
    -------
    dict
        Parsed JSON object.

    Raises
    ------
    ValueError
        If the Content-Type header is missing or not `application/json`,
        if the body exceeds ``MAX_BODY_SIZE``, or if JSON decoding fails.
    """
    # Retrieve headers and body
    headers = req.get("headers", {})
    if not isinstance(headers, dict):
        raise ValueError("Headers must be a dictionary.")

    # Normalize header names to lowercase for case‑insensitive comparison
    headers_lower = {k.lower(): v for k, v in headers.items()}

    content_type = headers_lower.get("content-type")
    if not content_type:
        raise ValueError("Missing 'Content-Type' header.")
    # Accept media type with parameters (e.g., application/json; charset=utf-8)
    if not content_type.lower().startswith("application/json"):
        raise ValueError(
            f"Unsupported Content-Type '{content_type}'. Expected 'application/json'."
        )

    # Retrieve body
    body = req.get("body")
    if body is None:
        raise ValueError("Missing request body.")
    if isinstance(body, bytes):
        try:
            body_str = body.decode("utf-8")
        except Exception as exc:
            raise ValueError(f"Failed to decode body bytes: {exc}") from exc
    elif isinstance(body, str):
        body_str = body
    else:
        raise ValueError("Body must be bytes or str.")

    # Enforce size limit
    if len(body_str.encode("utf-8")) > MAX_BODY_SIZE:
        raise ValueError(f"Request body exceeds the maximum allowed size of {MAX_BODY_SIZE} bytes.")

    # Parse JSON
    try:
        parsed = json.loads(body_str)
    except json.JSONDecodeError as exc:
        raise ValueError(f"Malformed JSON: {exc}") from exc

    if not isinstance(parsed, dict):
        raise ValueError("JSON payload must be an object (dictionary).")

    return parsed