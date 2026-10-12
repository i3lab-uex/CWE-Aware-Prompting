import json
from typing import Any, Dict

def process_json_input(req: Dict[str, Any]) -> Dict[str, Any]:
    """
    Parse a JSON request body from a FastAPI-like request dictionary.

    Parameters
    ----------
    req : dict
        A dictionary containing the HTTP headers and body of the incoming request.
        Expected keys:
            - "headers": a mapping-like object containing HTTP headers.
            - "body": the raw request body (str or bytes).

    Returns
    -------
    dict
        The parsed JSON payload.

    Raises
    ------
    ValueError
        If the Content-Type header does not indicate JSON or if JSON decoding fails.
    """
    # Validate presence of headers and body
    if not isinstance(req, dict):
        raise ValueError("Request must be a dictionary.")
    headers = req.get("headers")
    body = req.get("body")

    if headers is None or body is None:
        raise ValueError("Request must contain 'headers' and 'body' keys.")

    # Ensure headers is a mapping
    if not hasattr(headers, "get"):
        raise ValueError("Headers must be a mapping-like object.")

    # Check Content-Type
    content_type = headers.get("Content-Type") or headers.get("content-type")
    if not isinstance(content_type, str) or "application/json" not in content_type.lower():
        raise ValueError("Content-Type must be application/json.")

    # Ensure body is a string (decode bytes if necessary)
    if isinstance(body, bytes):
        try:
            body = body.decode("utf-8")
        except Exception as exc:  # pragma: no cover
            raise ValueError("Failed to decode body bytes as UTF-8.") from exc

    if not isinstance(body, str):
        raise ValueError("Body must be a string or bytes containing JSON.")

    # Parse JSON
    try:
        parsed = json.loads(body)
    except json.JSONDecodeError as exc:  # pragma: no cover
        raise ValueError(f"Malformed JSON: {exc.msg}") from exc

    if not isinstance(parsed, dict):
        raise ValueError("JSON payload must be an object (dictionary).")

    return parsed