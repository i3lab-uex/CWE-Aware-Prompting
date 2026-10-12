import json
from typing import Dict, Any

def decode_json_request(req: Dict[str, Any]) -> Dict[str, Any]:
    """
    Parse and validate the body of an incoming JSON request.

    Parameters
    ----------
    req : dict
        A dictionary representing the HTTP request. It must contain a
        'headers' key (mapping header names to values) and a 'body'
        key containing the raw request payload.

    Returns
    -------
    dict
        The decoded JSON body as a Python dictionary.

    Raises
    ------
    ValueError
        If the Content-Type header is missing or not application/json.
        If the body cannot be decoded as valid JSON.

    Notes
    -----
    The function does not perform any CSRF protection.  CSRF concerns
    should be handled by higher‑level middleware or the framework itself.
    """
    # Retrieve headers (case‑insensitive)
    headers = {k.lower(): v for k, v in req.get("headers", {}).items()}
    content_type = headers.get("content-type")

    if not content_type or "application/json" not in content_type.lower():
        raise ValueError(
            f"Unsupported Content-Type: {content_type!r}. Expected 'application/json'."
        )

    body = req.get("body", "")
    if isinstance(body, bytes):
        # FastAPI often provides body as bytes; decode to str
        try:
            body = body.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise ValueError(f"Body is not valid UTF-8: {exc}") from exc

    if not isinstance(body, str):
        raise ValueError(f"Body must be a string or bytes; got {type(body).__name__}")

    try:
        parsed = json.loads(body)
    except json.JSONDecodeError as exc:
        raise ValueError(f"Invalid JSON payload: {exc}") from exc

    if not isinstance(parsed, dict):
        raise ValueError(
            f"JSON payload must be an object (dict), got {type(parsed).__name__}"
        )

    return parsed