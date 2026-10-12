import json
from typing import Dict, Any

def validate_and_parse_json(incoming_req: Dict[str, Any]) -> Dict[str, Any]:
    """
    Validate that an incoming FastAPI request is JSON and parse its body.

    Parameters
    ----------
    incoming_req : dict
        Dictionary containing at least the keys ``headers`` and ``body``.
        The ``headers`` value should be a mapping of header names to values,
        and the ``body`` should be a JSON string (or bytes).

    Returns
    -------
    dict
        The parsed request body as a Python dictionary.

    Raises
    ------
    ValueError
        If the Content-Type header is missing or does not indicate JSON.
        If the body cannot be parsed as valid JSON.
    """
    # Extract headers and body
    headers = incoming_req.get("headers", {})
    if not isinstance(headers, dict):
        raise ValueError("Headers must be a dictionary")

    # Normalize header keys to lowercase for case‑insensitive lookup
    content_type = None
    for key, value in headers.items():
        if key.lower() == "content-type":
            content_type = str(value).lower()
            break

    if not content_type or not content_type.startswith("application/json"):
        raise ValueError(
            "Content-Type must be set to application/json or a compatible media type"
        )

    body = incoming_req.get("body")
    if body is None:
        raise ValueError("Request body is missing")

    # Ensure the body is a string or bytes; if bytes, decode using UTF‑8
    if isinstance(body, bytes):
        try:
            body = body.decode("utf-8")
        except Exception as exc:
            raise ValueError(f"Unable to decode request body: {exc}") from exc
    elif not isinstance(body, str):
        raise ValueError("Request body must be a string or bytes")

    # Parse JSON
    try:
        parsed = json.loads(body)
    except json.JSONDecodeError as exc:
        raise ValueError(f"Malformed JSON: {exc}") from exc

    if not isinstance(parsed, dict):
        raise ValueError("Parsed JSON must be an object (dictionary)")

    return parsed