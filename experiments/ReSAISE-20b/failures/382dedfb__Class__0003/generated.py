import json
from typing import Dict, Any

def validate_and_parse_json(incoming_req: Dict[str, Any]) -> Dict[str, Any]:
    """
    Validate the Content-Type header and parse a JSON body from an incoming request.

    Parameters
    ----------
    incoming_req : dict
        A dictionary containing the HTTP request information. It must include:
            - 'headers': a dict of request headers.
            - 'body': the raw body payload as a string or bytes.

    Returns
    -------
    dict
        The parsed JSON object from the request body.

    Raises
    ------
    ValueError
        If the Content-Type header is missing or does not indicate JSON.
        If the body cannot be parsed as valid JSON.
    """
    # 1. Retrieve headers, normalising case for comparison
    raw_headers = incoming_req.get("headers", {})
    if not isinstance(raw_headers, dict):
        raise ValueError("Headers must be a dictionary.")

    # Convert header names to lowercase for case-insensitive matching
    headers = {k.lower(): v for k, v in raw_headers.items()}

    # 2. Check content-type
    content_type = headers.get("content-type")
    if not content_type or "application/json" not in content_type.lower():
        raise ValueError("Content-Type must be application/json.")

    # 3. Retrieve body
    body = incoming_req.get("body")
    if body is None:
        raise ValueError("Request body missing.")

    # Body may be bytes; decode to string if necessary
    if isinstance(body, bytes):
        try:
            body_str = body.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise ValueError("Body is not valid UTF-8.") from exc
    elif isinstance(body, str):
        body_str = body
    else:
        raise ValueError("Body must be a string or bytes.")

    # 4. Parse JSON
    try:
        parsed = json.loads(body_str)
    except json.JSONDecodeError as exc:
        raise ValueError("Malformed JSON in request body.") from exc

    # 5. Ensure parsed object is a dict (JSON objects)
    if not isinstance(parsed, dict):
        raise ValueError("Parsed JSON must be an object (dictionary).")

    return parsed