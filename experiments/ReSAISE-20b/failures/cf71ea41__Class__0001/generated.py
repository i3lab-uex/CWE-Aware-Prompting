import json
from typing import Dict, Any


def process_json_payload(req_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Validate and parse the JSON body of an HTTP request.

    Parameters
    ----------
    req_data : dict
        A dictionary containing the HTTP request data. It must have at least two keys:
        - ``headers``: a mapping of header names to values.
        - ``body``: the raw request body as a string.

    Returns
    -------
    dict
        The parsed JSON object from the request body.

    Raises
    ------
    ValueError
        If the ``Content-Type`` header does not indicate a JSON-compatible type.
        If the request body is not valid JSON.
    """
    # Ensure required keys exist
    if "headers" not in req_data or "body" not in req_data:
        raise ValueError("Request data must contain 'headers' and 'body' keys")

    headers = req_data["headers"]
    body = req_data["body"]

    # Normalise header names to lower case for case‑insensitive lookup
    content_type = None
    for key, value in headers.items():
        if key.lower() == "content-type":
            content_type = value
            break

    # Verify that the content type indicates JSON
    if not content_type or "application/json" not in content_type.lower():
        raise ValueError("Content-Type must be application/json")

    # Attempt to parse the body as JSON
    try:
        parsed = json.loads(body)
    except (json.JSONDecodeError, TypeError) as exc:
        raise ValueError("Malformed JSON in request body") from exc

    # Ensure the parsed object is a dictionary (typical for request bodies)
    if not isinstance(parsed, dict):
        raise ValueError("JSON body must be an object (dictionary)")

    return parsed