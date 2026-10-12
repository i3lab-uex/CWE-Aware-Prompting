import json
from typing import Any, Dict

def parse_json_request(request: Dict[str, Any]) -> Dict[str, Any]:
    """
    Parse and validate a JSON request body.

    Parameters
    ----------
    request : dict
        A dictionary containing at least a 'body' key, which may be a string,
        bytes, or already-decoded JSON.

    Returns
    -------
    dict
        The decoded request body as a dictionary.

    Raises
    ------
    ValueError
        If JSON decoding fails or the body cannot be processed into a dictionary.
    """
    if not isinstance(request, dict):
        raise ValueError("Request must be a dictionary")

    # Retrieve the body; it may not exist
    if "body" not in request:
        raise ValueError("Missing 'body' in request")

    body = request["body"]

    # If the body is already a dict, return it directly
    if isinstance(body, dict):
        return body

    # If the body is bytes, decode to string
    if isinstance(body, (bytes, bytearray)):
        try:
            body = body.decode("utf-8")
        except Exception as exc:
            raise ValueError(f"Unable to decode body bytes: {exc}") from exc

    # If the body is a string, attempt JSON parsing
    if isinstance(body, str):
        try:
            decoded = json.loads(body)
        except json.JSONDecodeError as exc:
            raise ValueError(f"JSON decoding failed: {exc}") from exc
    else:
        # Unsupported type for body
        raise ValueError(f"Unsupported body type: {type(body).__name__}")

    # Ensure the decoded JSON is a dictionary
    if not isinstance(decoded, dict):
        raise ValueError("Decoded JSON must be an object (dictionary)")

    return decoded