import json
from typing import Dict, Any


def process_json_payload(req_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Validate and parse the JSON payload from an HTTP request.

    Parameters
    ----------
    req_data : dict
        A dictionary containing the request headers under the key 'headers'
        and the raw body under the key 'body'.

    Returns
    -------
    dict
        The parsed JSON object.

    Raises
    ------
    ValueError
        If the content‑type is not a JSON compatible type.
        If the body cannot be decoded as valid JSON.
    """
    # 1. Extract headers and body
    headers = req_data.get("headers", {})
    raw_body = req_data.get("body")

    # 2. Validate Content‑Type header
    content_type = headers.get("Content-Type") or headers.get("content-type")
    if not isinstance(content_type, str):
        raise ValueError("Missing or non‑string Content-Type header.")
    # Accept common JSON MIME types
    if not content_type.lower().startswith("application/json"):
        raise ValueError(f"Unsupported Content-Type: {content_type}")

    # 3. Ensure body is a string or bytes
    if raw_body is None:
        raise ValueError("Missing request body.")
    if isinstance(raw_body, bytes):
        try:
            raw_body = raw_body.decode("utf-8")
        except Exception as exc:
            raise ValueError(f"Body decoding error: {exc}") from exc
    elif not isinstance(raw_body, str):
        raise ValueError("Request body must be a string or bytes.")

    # 4. Parse JSON
    try:
        parsed = json.loads(raw_body)
    except json.JSONDecodeError as exc:
        raise ValueError(f"Malformed JSON: {exc}") from exc

    # 5. Ensure the result is a dictionary
    if not isinstance(parsed, dict):
        raise ValueError("JSON payload must be an object (dict).")

    return parsed