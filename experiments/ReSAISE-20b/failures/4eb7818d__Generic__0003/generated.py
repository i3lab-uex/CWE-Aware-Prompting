import json
from typing import Any, Dict

def parse_json_request(request: Dict[str, Any]) -> Dict[str, Any]:
    """
    Parse and validate a JSON request body.

    Parameters
    ----------
    request : dict
        The incoming request object. It must contain a ``body`` key with
        the raw JSON payload (as a string or bytes).

    Returns
    -------
    dict
        The decoded JSON object.

    Raises
    ------
    ValueError
        If the request does not contain a body, or if JSON decoding fails,
        or if the decoded object is not a dictionary.
    """
    # Ensure the request contains a body
    if "body" not in request:
        raise ValueError("Missing 'body' in the request")

    body = request["body"]

    # Accept both string and bytes representations of JSON
    if isinstance(body, bytes):
        try:
            body = body.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise ValueError(f"Body bytes could not be decoded: {exc}") from exc
    elif not isinstance(body, str):
        raise ValueError("Request body must be a string or bytes")

    # Parse the JSON payload
    try:
        data = json.loads(body)
    except json.JSONDecodeError as exc:
        raise ValueError(f"JSON decoding failed: {exc}") from exc

    # Ensure the payload is a dictionary
    if not isinstance(data, dict):
        raise ValueError("JSON payload must be an object (dictionary)")

    return data