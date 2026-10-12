import json
from typing import Dict

def validate_and_parse_json(incoming_req: Dict) -> Dict:
    """
    Validate the request's Content-Type header and parse its JSON body.

    Parameters
    ----------
    incoming_req : dict
        Dictionary containing request data. Expected keys:
            - 'headers' (dict): HTTP headers.
            - 'body' (str or bytes): Raw request body.

    Returns
    -------
    dict
        Parsed JSON content from the request body.

    Raises
    ------
    ValueError
        If the Content-Type header is missing or not JSON-compatible.
        If the body cannot be parsed as valid JSON.
    """
    # 1. Retrieve headers and ensure they exist
    headers = incoming_req.get("headers")
    if not isinstance(headers, dict):
        raise ValueError("Missing or malformed headers in request")

    # 2. Validate Content-Type header
    content_type = headers.get("Content-Type") or headers.get("content-type")
    if not content_type:
        raise ValueError("Missing Content-Type header")

    # Accept common JSON media types
    json_media_types = [
        "application/json",
        "application/ld+json",
        "application/vnd.api+json",
    ]
    if not any(ct.lower() == mt for ct in [content_type] for mt in json_media_types):
        raise ValueError(f"Unsupported Content-Type: {content_type}")

    # 3. Retrieve and decode the body
    raw_body = incoming_req.get("body")
    if raw_body is None:
        raise ValueError("Missing request body")

    # Ensure the body is a string for json.loads
    if isinstance(raw_body, bytes):
        try:
            raw_body = raw_body.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise ValueError("Body contains invalid UTF‑8") from exc

    if not isinstance(raw_body, str):
        raise ValueError("Body must be a string or bytes")

    # 4. Parse JSON
    try:
        parsed = json.loads(raw_body)
    except json.JSONDecodeError as exc:
        raise ValueError("Malformed JSON in request body") from exc

    # 5. Return parsed data
    return parsed