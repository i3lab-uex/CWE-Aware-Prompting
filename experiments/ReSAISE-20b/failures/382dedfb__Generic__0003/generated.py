import json
from typing import Any, Dict

def validate_and_parse_json(incoming_req: Dict[str, Any]) -> Dict[str, Any]:
    """
    Validate that the incoming request contains a JSON body and parse it.

    Parameters
    ----------
    incoming_req : dict
        Dictionary containing at least the keys 'headers' and 'body'.
        * `headers` must be a mapping of header names to values.
        * `body` can be either a JSON string or already a dict.

    Returns
    -------
    dict
        The parsed request body as a dictionary.

    Raises
    ------
    ValueError
        If the Content-Type header is missing or not a JSON-compatible value.
        If the body cannot be parsed as JSON.
    """
    # Ensure required keys exist
    if "headers" not in incoming_req or "body" not in incoming_req:
        raise ValueError("Request must contain 'headers' and 'body' keys")

    headers = incoming_req["headers"]
    body = incoming_req["body"]

    # Normalize header names to lower case for comparison
    content_type = headers.get("content-type") or headers.get("Content-Type")
    if not isinstance(content_type, str):
        raise ValueError("Missing or invalid Content-Type header")

    # Accept common JSON content types
    json_content_types = {
        "application/json",
        "application/ld+json",
        "application/vnd.api+json",
    }
    if not any(ct in content_type.lower() for ct in json_content_types):
        raise ValueError(f"Unsupported Content-Type: {content_type}")

    # If body is already a dict, return it directly
    if isinstance(body, dict):
        return body

    # If body is a bytes object, decode to string
    if isinstance(body, (bytes, bytearray)):
        try:
            body = body.decode("utf-8")
        except Exception as exc:
            raise ValueError("Body bytes could not be decoded to UTF-8") from exc

    # If body is a string, attempt JSON parsing
    if isinstance(body, str):
        try:
            parsed = json.loads(body)
        except json.JSONDecodeError as exc:
            raise ValueError("Malformed JSON in request body") from exc
        if not isinstance(parsed, dict):
            raise ValueError("JSON payload must be an object (dict)")
        return parsed

    # Unsupported body type
    raise ValueError("Request body must be a JSON string or dict")