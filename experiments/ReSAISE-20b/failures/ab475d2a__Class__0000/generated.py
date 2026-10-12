import json
from typing import Any, Dict

MAX_BODY_SIZE = 1_048_576  # 1 MiB limit to mitigate large payload attacks


def decode_json_request(req: Dict[str, Any]) -> Dict[str, Any]:
    """
    Parse and validate the body of an incoming JSON request.

    Parameters
    ----------
    req : dict
        A dictionary representing the HTTP request. Expected keys:
            - 'headers': a mapping of header names to values.
            - 'body'   : the raw request body as bytes or string.

    Returns
    -------
    dict
        The decoded JSON payload.

    Raises
    ------
    ValueError
        If the request content type is not acceptable or if JSON decoding fails.
    """
    # 1. Validate the Content-Type header
    headers = req.get("headers", {})
    content_type = (
        next((v for k, v in headers.items() if k.lower() == "content-type"), None)
        or ""
    ).lower()

    # Accept only application/json (with optional charset)
    if not content_type.startswith("application/json"):
        raise ValueError(
            "Unsupported Content-Type: only application/json is accepted."
        )

    # 2. Retrieve the body and enforce size limit
    body = req.get("body")
    if body is None:
        raise ValueError("Missing request body.")

    # Convert bytes to str if necessary
    if isinstance(body, bytes):
        try:
            body_text = body.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise ValueError(f"Body is not valid UTF-8: {exc}") from exc
    elif isinstance(body, str):
        body_text = body
    else:
        raise ValueError("Body must be bytes or str.")

    if len(body_text) > MAX_BODY_SIZE:
        raise ValueError(f"Request body exceeds maximum allowed size of {MAX_BODY_SIZE} bytes.")

    # 3. Parse JSON safely
    try:
        payload = json.loads(body_text, strict=True)
    except json.JSONDecodeError as exc:
        raise ValueError(f"Invalid JSON payload: {exc}") from exc

    if not isinstance(payload, dict):
        raise ValueError("JSON payload must be an object (dictionary).")

    return payload