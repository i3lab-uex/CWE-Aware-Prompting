import json
from typing import Dict, Any


def validate_and_parse_json(incoming_req: Dict[str, Any]) -> Dict[str, Any]:
    """
    Validate that the incoming request contains a JSON body and parse it.

    Parameters
    ----------
    incoming_req : dict
        Dictionary containing two keys:
            - 'headers': a mapping of HTTP headers (case‑insensitive)
            - 'body'   : the raw request body as a string or bytes

    Returns
    -------
    dict
        The parsed JSON payload.

    Raises
    ------
    ValueError
        If the `Content-Type` header is missing or not JSON compatible.
    ValueError
        If the body cannot be decoded as valid JSON.
    """
    # 1. Retrieve headers and body
    try:
        headers = incoming_req["headers"]
        raw_body = incoming_req["body"]
    except KeyError as exc:
        raise ValueError("Missing 'headers' or 'body' in request") from exc

    # 2. Normalise header keys to lower case for case‑insensitive lookup
    headers_normalized = {
        k.lower(): v for k, v in headers.items()
    }

    # 3. Validate Content-Type header
    content_type = headers_normalized.get("content-type")
    if not content_type or "application/json" not in content_type.lower():
        raise ValueError(
            f"Unsupported Content-Type: {content_type!r}. "
            "Expected application/json."
        )

    # 4. Ensure body is a string; if bytes, decode using UTF-8
    if isinstance(raw_body, bytes):
        try:
            raw_body = raw_body.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise ValueError("Body is not valid UTF-8 encoded text") from exc
    elif not isinstance(raw_body, str):
        raise ValueError(
            f"Body must be a string or bytes, got {type(raw_body).__name__}"
        )

    # 5. Parse JSON payload
    try:
        parsed_body = json.loads(raw_body)
    except json.JSONDecodeError as exc:
        raise ValueError(f"Malformed JSON: {exc.msg}") from exc

    # 6. Ensure the parsed payload is a dictionary (as expected by the API)
    if not isinstance(parsed_body, dict):
        raise ValueError(
            f"JSON payload must be an object (dict), got {type(parsed_body).__name__}"
        )

    return parsed_body