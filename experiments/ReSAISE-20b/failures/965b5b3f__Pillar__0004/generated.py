import json
from typing import Dict, Any

def process_json_request(req_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Parse and validate the body of an incoming JSON request.

    Parameters
    ----------
    req_data : dict
        Dictionary containing the request headers and body. Expected keys:
            - "headers": mapping of header names to values
            - "body": raw request body (bytes or str)

    Returns
    -------
    dict
        Parsed JSON content as a Python dictionary.

    Raises
    ------
    ValueError
        If the Content-Type header is missing or not `application/json`.
        If the body cannot be decoded as valid JSON.
    """
    # Ensure required keys exist
    if "headers" not in req_data or "body" not in req_data:
        raise ValueError("Request data must contain 'headers' and 'body' keys")

    headers = req_data["headers"]
    body = req_data["body"]

    # Normalise header names to lower case for comparison
    content_type = headers.get("Content-Type") or headers.get("content-type")
    if not content_type:
        raise ValueError("Missing Content-Type header")

    # Accept only application/json (allow optional charset)
    if not content_type.lower().startswith("application/json"):
        raise ValueError(
            f"Unsupported Content-Type '{content_type}'. Expected 'application/json'"
        )

    # Convert body to string if it is bytes
    if isinstance(body, bytes):
        try:
            body_str = body.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise ValueError("Body is not valid UTF-8 encoded text") from exc
    elif isinstance(body, str):
        body_str = body
    else:
        raise ValueError("Body must be bytes or str")

    # Parse JSON safely
    try:
        parsed = json.loads(body_str)
    except json.JSONDecodeError as exc:
        raise ValueError("Body is not valid JSON") from exc

    if not isinstance(parsed, dict):
        raise ValueError("JSON payload must be an object (dict)")

    return parsed