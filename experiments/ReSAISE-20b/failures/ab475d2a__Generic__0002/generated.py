import json
from typing import Any, Dict


def decode_json_request(req: Dict[str, Any]) -> Dict[str, Any]:
    """
    Parse and validate the body of an incoming JSON request.

    Parameters
    ----------
    req : dict
        Dictionary containing at least two keys:
            - 'headers': a mapping of request headers (case‑insensitive)
            - 'body'   : the raw body payload as bytes or str

    Returns
    -------
    dict
        The decoded JSON payload.

    Raises
    ------
    ValueError
        If the Content‑Type is not application/json or a JSON parsing error occurs.
    """
    # Retrieve headers (case‑insensitive)
    headers = {k.lower(): v for k, v in req.get("headers", {}).items()}

    content_type = headers.get("content-type")
    if not content_type or "application/json" not in content_type.lower():
        raise ValueError(
            f"Unsupported Content-Type '{content_type}'. Expected 'application/json'."
        )

    # Body can be bytes or str; convert to str if needed
    body = req.get("body")
    if body is None:
        raise ValueError("Request body is missing.")

    if isinstance(body, bytes):
        try:
            body_text = body.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise ValueError(f"Body decoding failed: {exc}") from exc
    elif isinstance(body, str):
        body_text = body
    else:
        raise ValueError(f"Unsupported body type: {type(body).__name__}")

    # Limit the size to avoid DoS attacks (example: 1 MB)
    MAX_BODY_SIZE = 1 * 1024 * 1024
    if len(body_text) > MAX_BODY_SIZE:
        raise ValueError("Request body too large.")

    try:
        payload = json.loads(body_text)
    except json.JSONDecodeError as exc:
        raise ValueError(f"Invalid JSON: {exc}") from exc

    if not isinstance(payload, dict):
        raise ValueError("JSON payload must be an object (dict).")

    return payload