import json
from typing import Any, Dict


def process_json_input(req: Dict[str, Any]) -> Dict[str, Any]:
    """
    Parse the JSON body of a FastAPI request.

    Parameters
    ----------
    req : dict
        A dictionary representing the incoming HTTP request.
        Expected keys:
            - "headers": a mapping of header names to values
            - "body"   : the raw request body as a string or bytes

    Returns
    -------
    dict
        The parsed JSON object.

    Raises
    ------
    ValueError
        If the Content-Type header is missing or not `application/json`,
        or if the body cannot be decoded as JSON.
    """
    # Validate presence of headers and body
    if not isinstance(req, dict):
        raise ValueError("Request must be a dictionary.")
    headers = req.get("headers")
    body = req.get("body")

    if headers is None or not isinstance(headers, dict):
        raise ValueError("Request headers are missing or malformed.")
    if body is None:
        raise ValueError("Request body is missing.")

    # Normalise header names to lower-case for case-insensitive lookup
    headers_lc = {k.lower(): v for k, v in headers.items()}

    content_type = headers_lc.get("content-type")
    if not content_type or "application/json" not in content_type.lower():
        raise ValueError(
            f"Invalid Content-Type: {content_type!r}. Expected application/json."
        )

    # Convert body to string if it's bytes
    if isinstance(body, bytes):
        try:
            body_str = body.decode("utf-8")
        except Exception as exc:
            raise ValueError(f"Failed to decode request body: {exc}") from exc
    elif isinstance(body, str):
        body_str = body
    else:
        raise ValueError("Request body must be a string or bytes.")

    # Parse JSON
    try:
        parsed = json.loads(body_str)
    except json.JSONDecodeError as exc:
        raise ValueError(f"Malformed JSON: {exc}") from exc

    if not isinstance(parsed, dict):
        raise ValueError("JSON payload must be an object (dictionary).")

    return parsed