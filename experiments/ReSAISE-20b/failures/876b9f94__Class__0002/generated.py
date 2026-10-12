import json
from typing import Dict

MAX_BODY_SIZE = 10 * 1024 * 1024  # 10 MB limit to mitigate DoS attacks


def process_json_input(req: Dict) -> Dict:
    """
    Parse and validate a JSON request body from a FastAPI-style request dictionary.

    Parameters
    ----------
    req : dict
        Dictionary containing at least two keys:
            - 'headers': a mapping of header names to values (case‑insensitive).
            - 'body'   : the raw request body as a bytes or string object.

    Returns
    -------
    dict
        The decoded JSON payload.

    Raises
    ------
    ValueError
        If the 'Content-Type' header is missing or not set to a JSON media type.
        If the body exceeds ``MAX_BODY_SIZE``.
        If the body cannot be decoded as valid JSON.
    """
    # 1. Validate headers exist
    if not isinstance(req, dict):
        raise ValueError("Request must be a dictionary.")
    headers = req.get("headers")
    if not isinstance(headers, dict):
        raise ValueError("Request headers must be a dictionary.")

    # 2. Check Content-Type header (case‑insensitive)
    content_type = None
    for key, value in headers.items():
        if key.lower() == "content-type":
            content_type = value
            break

    if not content_type:
        raise ValueError("Missing 'Content-Type' header.")
    if "application/json" not in content_type.lower():
        raise ValueError(
            f"Unsupported Content-Type '{content_type}'. Expected 'application/json'."
        )

    # 3. Retrieve body and enforce size limit
    body = req.get("body")
    if body is None:
        raise ValueError("Missing request body.")
    # Convert bytes to string if necessary
    if isinstance(body, bytes):
        try:
            body_str = body.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise ValueError(f"Body is not valid UTF-8: {exc}") from exc
    elif isinstance(body, str):
        body_str = body
    else:
        raise ValueError("Body must be a bytes or string object.")

    if len(body_str) > MAX_BODY_SIZE:
        raise ValueError(f"Request body exceeds maximum allowed size of {MAX_BODY_SIZE} bytes.")

    # 4. Parse JSON safely
    try:
        parsed = json.loads(body_str)
    except json.JSONDecodeError as exc:
        raise ValueError(f"Malformed JSON: {exc}") from exc

    if not isinstance(parsed, dict):
        raise ValueError("JSON payload must be an object (dictionary).")

    return parsed