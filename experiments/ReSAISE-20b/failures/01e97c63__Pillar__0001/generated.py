import json
from typing import Dict, Any


def handle_json_input(client_request: Dict[str, Any]) -> Dict[str, Any]:
    """
    Validate and parse a JSON request body.

    Parameters
    ----------
    client_request : dict
        Dictionary containing HTTP request headers and body. Expected keys:
            - 'headers': Mapping of header names to values.
            - 'body'   : Raw request body, either a ``str`` or ``bytes``.

    Returns
    -------
    dict
        Parsed JSON content as a Python dictionary.

    Raises
    ------
    ValueError
        If the ``Content-Type`` header is not JSON-compatible.
        If the body cannot be parsed as valid JSON.
    """
    # 1. Extract headers and ensure Content-Type is application/json (case‑insensitive)
    headers = client_request.get("headers", {})
    content_type: str | None = None
    for key, value in headers.items():
        if key.lower() == "content-type":
            content_type = str(value)
            break

    if not content_type or not content_type.lower().startswith("application/json"):
        raise ValueError(
            f"Unsupported Content-Type: {content_type!r}. Expected application/json."
        )

    # 2. Retrieve body
    raw_body = client_request.get("body")
    if raw_body is None:
        raise ValueError("Missing request body.")

    # 3. Ensure body is a string (decode bytes if necessary)
    if isinstance(raw_body, bytes):
        try:
            raw_body = raw_body.decode("utf-8")
        except Exception as exc:  # pragma: no cover
            raise ValueError("Request body could not be decoded as UTF‑8.") from exc

    if not isinstance(raw_body, str):
        raise ValueError(f"Request body must be a string or bytes, got {type(raw_body).__name__}.")

    # 4. Parse JSON
    try:
        parsed = json.loads(raw_body)
    except json.JSONDecodeError as exc:  # pragma: no cover
        raise ValueError("Malformed JSON in request body.") from exc

    # 5. Ensure parsed content is a dictionary (typical for API payloads)
    if not isinstance(parsed, dict):
        raise ValueError("JSON body must represent an object (dictionary).")

    return parsed