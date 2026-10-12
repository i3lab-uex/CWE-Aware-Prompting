import json
from typing import Dict, Any

def process_json_input(req: Dict[str, Any]) -> Dict[str, Any]:
    """
    Parse the JSON body of an incoming FastAPI request.

    Parameters
    ----------
    req : dict
        A dictionary containing the HTTP headers and body of the incoming request.
        Expected keys are:
            - "headers": a mapping-like object with header names as keys (case-insensitive).
            - "body": the raw request body, either a str or bytes.

    Returns
    -------
    dict
        The parsed JSON object if the request body is valid JSON.

    Raises
    ------
    ValueError
        If the Content-Type header does not contain 'application/json'.
        If the body cannot be decoded as valid JSON.
    """
    # 1. Validate Content-Type header
    headers = req.get("headers", {})
    if not isinstance(headers, dict):
        raise ValueError("Headers must be a dictionary")

    # Normalize header names to lower case for case-insensitive lookup
    content_type = next(
        (value for key, value in headers.items() if key.lower() == "content-type"),
        None,
    )
    if content_type is None or "application/json" not in content_type.lower():
        raise ValueError("Invalid Content-Type. Expected application/json")

    # 2. Retrieve body
    body = req.get("body")
    if body is None:
        raise ValueError("Request body missing")

    # Convert bytes to str if necessary
    if isinstance(body, bytes):
        try:
            body = body.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise ValueError(f"Body decoding error: {exc}") from exc

    if not isinstance(body, str):
        raise ValueError("Body must be a string or bytes")

    # 3. Parse JSON
    try:
        parsed = json.loads(body)
    except json.JSONDecodeError as exc:
        raise ValueError(f"Malformed JSON: {exc}") from exc

    # 4. Ensure the parsed object is a dictionary
    if not isinstance(parsed, dict):
        raise ValueError("JSON body must be an object (dict)")

    return parsed