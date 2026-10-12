import json
from typing import Dict, Any


def handle_json_input(client_request: Dict[str, Any]) -> Dict[str, Any]:
    """
    Parse and validate a JSON request body.

    Parameters
    ----------
    client_request : dict
        Dictionary containing at least the keys ``headers`` and ``body``.
        * ``headers`` should be a mapping of header names to values
          (case-insensitive).
        * ``body`` should be a string or bytes containing the raw request
          payload.

    Returns
    -------
    dict
        The parsed JSON object as a Python dictionary.

    Raises
    ------
    ValueError
        If the ``Content-Type`` header is missing or does not indicate a
        JSON-compatible media type.
    ValueError
        If the body cannot be parsed as valid JSON.
    """
    # Ensure headers are present and case‑insensitive
    if not isinstance(client_request, dict):
        raise ValueError("client_request must be a dictionary")

    headers = client_request.get("headers")
    if not isinstance(headers, dict):
        raise ValueError("client_request must contain a 'headers' mapping")

    # Normalise header keys to lowercase for case‑insensitivity
    headers_lc = {k.lower(): v for k, v in headers.items()}

    content_type = headers_lc.get("content-type")
    if not content_type:
        raise ValueError("Missing 'Content-Type' header")

    # Accept common JSON media types
    json_media_types = {"application/json", "application/ld+json", "application/vnd.api+json"}
    if not any(ct.lower().startswith(mt) for mt in json_media_types for ct in [content_type]):
        raise ValueError(f"Unsupported Content-Type: {content_type}")

    body = client_request.get("body")
    if body is None:
        raise ValueError("Missing request body")

    # Convert bytes to str if necessary
    if isinstance(body, bytes):
        try:
            body_str = body.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise ValueError("Body is not valid UTF-8") from exc
    elif isinstance(body, str):
        body_str = body
    else:
        raise ValueError("Body must be a string or bytes")

    try:
        parsed = json.loads(body_str)
    except json.JSONDecodeError as exc:
        raise ValueError("Malformed JSON in request body") from exc

    if not isinstance(parsed, dict):
        raise ValueError("JSON payload must be an object (dictionary)")

    return parsed