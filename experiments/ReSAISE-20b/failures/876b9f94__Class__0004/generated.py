import json
from typing import Any, Dict

def process_json_input(req: Dict[str, Any]) -> Dict[str, Any]:
    """
    Parse the JSON body of a FastAPI request.

    Parameters
    ----------
    req : dict
        Dictionary containing the HTTP headers and body of the incoming request.
        Expected keys:
            - "headers": dict, mapping header names to values
            - "body": bytes or str, the raw request body

    Returns
    -------
    dict
        The parsed JSON object.

    Raises
    ------
    ValueError
        If the Content-Type header is missing or not `application/json`.
        If the body cannot be decoded as valid JSON.
    """
    # Validate presence of headers and body
    if not isinstance(req, dict):
        raise ValueError("Request must be a dictionary.")
    headers = req.get("headers")
    body = req.get("body")

    if not isinstance(headers, dict):
        raise ValueError("Request headers must be a dictionary.")
    if body is None:
        raise ValueError("Request body is missing.")

    # Normalize header names to lowercase for case‑insensitive comparison
    content_type = headers.get("content-type") or headers.get("Content-Type")
    if not content_type:
        raise ValueError("Missing Content-Type header.")
    # Only accept exact JSON media type (allow optional charset)
    if not content_type.lower().startswith("application/json"):
        raise ValueError(
            f"Unsupported Content-Type '{content_type}'. Expected 'application/json'."
        )

    # Decode body if bytes
    if isinstance(body, bytes):
        try:
            body_text = body.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise ValueError(f"Body is not valid UTF‑8: {exc}") from exc
    elif isinstance(body, str):
        body_text = body
    else:
        raise ValueError("Request body must be bytes or str.")

    # Parse JSON safely
    try:
        parsed = json.loads(body_text)
    except json.JSONDecodeError as exc:
        raise ValueError(f"Malformed JSON: {exc}") from exc

    if not isinstance(parsed, dict):
        raise ValueError("JSON payload must be an object (dictionary).")

    return parsed