import json
from typing import Any, Dict

def process_json_input(req: Dict[str, Any]) -> Dict:
    """
    Parse the JSON body of a FastAPI request.

    Parameters
    ----------
    req : dict
        A dictionary representing the HTTP request. Expected keys:
            - 'headers': a mapping of header names to values.
            - 'body'   : the raw request body (str or bytes).

    Returns
    -------
    dict
        The parsed JSON object.

    Raises
    ------
    ValueError
        If the Content-Type header is missing or not a JSON type.
        If the body cannot be decoded as valid JSON.
    """
    # Extract headers and body
    headers = req.get("headers", {})
    body   = req.get("body")

    # Ensure Content-Type is application/json (allow charset)
    content_type = headers.get("Content-Type") or headers.get("content-type")
    if not content_type:
        raise ValueError("Missing Content-Type header")

    # Normalize to lowercase for comparison
    ct_lower = content_type.lower()
    if not (ct_lower.startswith("application/json") or
            ct_lower == "text/json"):
        raise ValueError(f"Invalid Content-Type '{content_type}'. Expected application/json")

    # Ensure body is a string
    if isinstance(body, bytes):
        try:
            body = body.decode("utf-8")
        except Exception as exc:
            raise ValueError(f"Body decoding failed: {exc}") from exc
    elif not isinstance(body, str):
        raise ValueError("Request body must be a string or bytes")

    # Parse JSON
    try:
        data = json.loads(body)
    except json.JSONDecodeError as exc:
        raise ValueError(f"Malformed JSON: {exc}") from exc

    if not isinstance(data, dict):
        raise ValueError("JSON payload must be an object (dictionary)")

    return data