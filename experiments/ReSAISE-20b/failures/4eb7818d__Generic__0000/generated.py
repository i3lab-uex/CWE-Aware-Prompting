import json
from typing import Dict, Any


def parse_json_request(request: Dict[str, Any]) -> Dict[str, Any]:
    """
    Parse and validate the JSON body of a FastAPI request.

    Parameters
    ----------
    request : dict
        A dictionary representation of the incoming request, expected to contain:
            - ``headers`` : dict of HTTP headers
            - ``body``   : bytes or str containing the JSON payload

    Returns
    -------
    dict
        The decoded JSON object.

    Raises
    ------
    ValueError
        If the request body is missing, not a string/bytes, or cannot be decoded as JSON.
    """
    # Ensure request contains the expected keys
    if not isinstance(request, dict):
        raise ValueError("Request must be a dictionary.")

    headers = request.get("headers")
    body = request.get("body")

    if headers is None or not isinstance(headers, dict):
        raise ValueError("Request must contain a 'headers' dictionary.")

    if body is None:
        raise ValueError("Missing request body.")
    if not isinstance(body, (bytes, str)):
        raise ValueError("Request body must be a string or bytes object.")

    # Optionally check the Content-Type header
    content_type = headers.get("Content-Type", "").lower()
    if "application/json" not in content_type:
        raise ValueError("Unsupported Content-Type; expected application/json.")

    # Convert bytes to string if necessary
    if isinstance(body, bytes):
        try:
            body_str = body.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise ValueError(f"Body decoding error: {exc}") from exc
    else:
        body_str = body

    # Parse JSON safely
    try:
        data = json.loads(body_str)
    except json.JSONDecodeError as exc:
        raise ValueError(f"JSON decoding failed: {exc}") from exc

    if not isinstance(data, dict):
        raise ValueError("JSON payload must be an object (dictionary).")

    return data