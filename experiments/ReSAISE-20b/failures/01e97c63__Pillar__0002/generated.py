import json
from typing import Dict, Any


def handle_json_input(client_request: Dict[str, Any]) -> Dict[str, Any]:
    """
    Parse and validate a JSON request body.

    Parameters
    ----------
    client_request : dict
        A dictionary containing the HTTP request headers and body.  It must
        include at least the keys ``"headers"`` (a dict of header names to
        values) and ``"body"`` (the raw request body, either a string or
        bytes).

    Returns
    -------
    dict
        The parsed JSON payload.

    Raises
    ------
    ValueError
        If the ``Content-Type`` header is missing or does not indicate a JSON
        payload, or if the body cannot be decoded as valid JSON.
    """
    # Validate presence of headers and body
    if not isinstance(client_request, dict):
        raise ValueError("client_request must be a dictionary")

    headers = client_request.get("headers")
    body = client_request.get("body")

    if not isinstance(headers, dict):
        raise ValueError("headers must be a dictionary")
    if body is None:
        raise ValueError("body must be provided")

    # Normalize header names to lower-case for case-insensitive matching
    normalized_headers = {k.lower(): v for k, v in headers.items()}

    content_type = normalized_headers.get("content-type")
    if not content_type:
        raise ValueError("Missing Content-Type header")

    # Accept only application/json or compatible MIME types
    if not content_type.lower().startswith("application/json"):
        raise ValueError(f"Unsupported Content-Type: {content_type}")

    # Decode body if it is bytes
    if isinstance(body, bytes):
        try:
            body_text = body.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise ValueError("Body is not valid UTF-8") from exc
    elif isinstance(body, str):
        body_text = body
    else:
        raise ValueError("Body must be a string or bytes")

    # Parse JSON
    try:
        parsed = json.loads(body_text)
    except json.JSONDecodeError as exc:
        raise ValueError("Malformed JSON") from exc

    if not isinstance(parsed, dict):
        # In many APIs a non-dict JSON body is considered invalid
        raise ValueError("JSON payload must be an object (dict)")

    return parsed