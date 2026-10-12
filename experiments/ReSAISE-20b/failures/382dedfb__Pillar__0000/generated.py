import json
from typing import Any, Dict

def validate_and_parse_json(incoming_req: Dict[str, Any]) -> Dict[str, Any]:
    """
    Validate that the request contains a JSON body and parse it.

    Parameters
    ----------
    incoming_req : dict
        Dictionary containing at least two keys:
            - "headers": a mapping of header names to values.
            - "body": the raw request body (bytes or str).

    Returns
    -------
    dict
        The parsed JSON object.

    Raises
    ------
    ValueError
        If the Content-Type header is missing or not a JSON-compatible type.
        If the body cannot be decoded as valid JSON.
    """
    # Extract headers and body
    headers = incoming_req.get("headers", {})
    body = incoming_req.get("body")

    # Ensure headers is a mapping and perform case‑insensitive lookup
    if not isinstance(headers, dict):
        raise ValueError("Headers must be a dictionary")

    # Find Content-Type header in a case‑insensitive manner
    content_type = None
    for key, value in headers.items():
        if key.lower() == "content-type":
            content_type = str(value).lower()
            break

    if not content_type or "application/json" not in content_type:
        raise ValueError("Content-Type must be application/json")

    # Body must be bytes or str; decode if necessary
    if isinstance(body, bytes):
        try:
            body_str = body.decode("utf-8")
        except Exception as exc:
            raise ValueError(f"Body bytes could not be decoded: {exc}") from exc
    elif isinstance(body, str):
        body_str = body
    else:
        raise ValueError("Body must be a bytes or str instance")

    # Parse JSON safely
    try:
        parsed = json.loads(body_str, strict=True)
    except json.JSONDecodeError as exc:
        raise ValueError(f"Malformed JSON: {exc}") from exc

    if not isinstance(parsed, dict):
        raise ValueError("JSON body must be an object (dict)")

    return parsed