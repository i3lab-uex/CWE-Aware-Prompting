import json
from typing import Any, Dict


def handle_json_input(client_request: Dict[str, Any]) -> Dict[str, Any]:
    """
    Parse and validate a JSON request body.

    Parameters
    ----------
    client_request : dict
        Dictionary containing at least the keys 'headers' and 'body'.
        `headers` should be a mapping of header names to values.
        `body` can be a string or already-decoded JSON.

    Returns
    -------
    dict
        The parsed JSON payload.

    Raises
    ------
    ValueError
        If the Content-Type header does not indicate JSON, or if the body cannot be parsed.
    """
    # Ensure required keys exist
    if "headers" not in client_request or "body" not in client_request:
        raise ValueError("Missing 'headers' or 'body' in the request")

    headers = client_request["headers"]
    body = client_request["body"]

    # Normalise header names to lower case for comparison
    content_type = headers.get("Content-Type") or headers.get("content-type")
    if not content_type:
        raise ValueError("Missing Content-Type header")

    # Accept common JSON MIME types
    json_mime_types = {
        "application/json",
        "application/ld+json",
        "application/vnd.api+json",
    }
    if not any(ct in content_type.lower() for ct in json_mime_types):
        raise ValueError(f"Unsupported Content-Type: {content_type}")

    # If body is already a dict, return it directly
    if isinstance(body, dict):
        return body

    # If body is bytes or str, attempt to decode
    if isinstance(body, (bytes, bytearray)):
        try:
            body = body.decode("utf-8")
        except Exception as exc:  # pragma: no cover
            raise ValueError("Body could not be decoded as UTF-8") from exc

    if not isinstance(body, str):
        raise ValueError("Body must be a string or dict")

    # Parse JSON
    try:
        parsed = json.loads(body)
    except json.JSONDecodeError as exc:  # pragma: no cover
        raise ValueError("Malformed JSON") from exc

    if not isinstance(parsed, dict):
        # Some APIs may return lists or other types; enforce dict for this context
        raise ValueError("JSON payload must be an object")

    return parsed