import json
from typing import Dict

def process_json_input(req: Dict) -> Dict:
    """
    Parse the JSON body of a FastAPI request.

    Parameters
    ----------
    req : dict
        Dictionary containing the HTTP headers under 'headers' key and the raw body string under
        'body' key. Example:
            {
                "headers": {"content-type": "application/json"},
                "body": '{"key":"value"}'
            }

    Returns
    -------
    dict
        Parsed JSON object.

    Raises
    ------
    ValueError
        If the Content-Type header is missing or does not contain 'application/json'.
        If the body cannot be decoded as valid JSON.
    """
    # Retrieve headers and body
    headers = req.get("headers", {})
    body_raw = req.get("body")

    # Validate content type
    content_type = headers.get("content-type") or headers.get("Content-Type")
    if not content_type:
        raise ValueError("Missing Content-Type header.")
    if "application/json" not in content_type.lower():
        raise ValueError(f"Unsupported Content-Type: {content_type}. Expected application/json.")

    # Ensure body is a string
    if not isinstance(body_raw, str):
        raise ValueError("Request body must be a string containing JSON.")

    # Parse the JSON
    try:
        parsed = json.loads(body_raw)
    except json.JSONDecodeError as exc:
        raise ValueError(f"Malformed JSON: {exc.msg}") from None

    # Ensure the parsed result is a dictionary
    if not isinstance(parsed, dict):
        raise ValueError("JSON payload must be an object (dictionary).")

    return parsed