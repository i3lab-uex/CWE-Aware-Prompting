import json
from typing import Dict, Any

def process_json_input(req: Dict[str, Any]) -> Dict[str, Any]:
    """
    Parse a JSON request body from a FastAPI-style request dictionary.

    Parameters
    ----------
    req : dict
        A dictionary containing the HTTP headers and body of an incoming request.
        Expected keys:
            - "headers": a dict mapping header names to values
            - "body": the raw request body as bytes or str

    Returns
    -------
    dict
        The parsed JSON object.

    Raises
    ------
    ValueError
        If the Content-Type header is missing or not 'application/json',
        or if the body cannot be decoded as valid JSON.
    """
    # Retrieve headers and ensure they are a mapping
    headers = req.get("headers")
    if not isinstance(headers, dict):
        raise ValueError("Request headers are missing or malformed.")

    # Normalize header names to lowercase for case-insensitive comparison
    content_type = None
    for key, value in headers.items():
        if key.lower() == "content-type":
            content_type = str(value).strip()
            break

    if content_type is None:
        raise ValueError("Missing 'Content-Type' header.")
    # Only accept application/json (optionally with charset)
    if not content_type.lower().startswith("application/json"):
        raise ValueError(
            f"Unsupported Content-Type '{content_type}'. Expected 'application/json'."
        )

    # Retrieve the body
    body = req.get("body")
    if body is None:
        raise ValueError("Request body is missing.")

    # Body may be bytes or str; ensure we have a string
    if isinstance(body, bytes):
        try:
            body_str = body.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise ValueError("Request body is not valid UTF-8.") from exc
    elif isinstance(body, str):
        body_str = body
    else:
        raise ValueError("Request body must be bytes or str.")

    # Parse JSON safely
    try:
        parsed = json.loads(body_str)
    except json.JSONDecodeError as exc:
        raise ValueError(f"Malformed JSON: {exc.msg}") from exc

    if not isinstance(parsed, dict):
        raise ValueError("JSON payload must be an object (dictionary).")

    return parsed