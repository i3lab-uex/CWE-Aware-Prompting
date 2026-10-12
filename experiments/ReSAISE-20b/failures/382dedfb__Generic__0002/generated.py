import json
from typing import Dict, Any

def validate_and_parse_json(incoming_req: Dict[str, Any]) -> Dict[str, Any]:
    """
    Validate and parse the JSON body of an incoming HTTP request.

    Parameters
    ----------
    incoming_req : dict
        A dictionary containing at least the keys:
            - 'headers': a mapping of header names to values
            - 'body'   : the raw request body as a string

    Returns
    -------
    dict
        The parsed JSON payload.

    Raises
    ------
    ValueError
        If the request does not declare a JSON-compatible content type,
        or if the body cannot be parsed as valid JSON.
    """
    # Ensure required keys exist
    if not isinstance(incoming_req, dict):
        raise ValueError("incoming_req must be a dictionary")
    headers = incoming_req.get("headers", {})
    body = incoming_req.get("body")

    if not isinstance(headers, dict):
        raise ValueError("headers must be a dictionary")
    if body is None:
        raise ValueError("request body missing")

    # Normalise header names to lowercase for case‑insensitive lookup
    content_type = headers.get("content-type") or headers.get("Content-Type")
    if not content_type:
        raise ValueError("Missing Content-Type header")

    # Accept common JSON MIME types
    json_mime_types = {
        "application/json",
        "application/ld+json",
        "application/vnd.api+json",
    }
    # Allow wildcard like application/json; charset=utf-8
    def _is_json_type(ct: str) -> bool:
        ct = ct.split(";")[0].strip().lower()
        return ct in json_mime_types

    if not _is_json_type(content_type):
        raise ValueError(f"Unsupported Content-Type: {content_type}")

    # Parse the body safely
    try:
        parsed = json.loads(body)
    except (json.JSONDecodeError, TypeError) as exc:
        raise ValueError("Malformed JSON body") from exc

    if not isinstance(parsed, dict):
        # For most APIs the payload should be an object
        raise ValueError("JSON body must be an object (dict)")

    return parsed