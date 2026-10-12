import json
from typing import Dict, Any


def process_json_payload(req_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Parse and validate a JSON payload from an HTTP request.

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
        If the Content-Type header does not indicate a JSON-compatible type,
        or if the body is not valid JSON.
    """
    # Ensure required keys exist
    headers = req_data.get("headers")
    body = req_data.get("body")

    if not isinstance(headers, dict):
        raise ValueError("Request headers must be a dictionary.")
    if body is None:
        raise ValueError("Request body is missing.")

    # Validate Content-Type header
    content_type = headers.get("Content-Type") or headers.get("content-type")
    if not content_type:
        raise ValueError("Missing Content-Type header.")
    # Accept common JSON MIME types
    if not any(ct in content_type.lower() for ct in ("application/json", "application/*+json")):
        raise ValueError(f"Unsupported Content-Type: {content_type}")

    # Ensure body is a string or bytes
    if isinstance(body, bytes):
        try:
            body = body.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise ValueError("Body is not valid UTF-8 encoded text.") from exc
    if not isinstance(body, str):
        raise ValueError("Body must be a string or bytes.")

    # Parse JSON safely
    try:
        parsed = json.loads(body)
    except json.JSONDecodeError as exc:
        raise ValueError("Malformed JSON in request body.") from exc

    if not isinstance(parsed, dict):
        raise ValueError("JSON payload must be an object (dictionary).")

    return parsed