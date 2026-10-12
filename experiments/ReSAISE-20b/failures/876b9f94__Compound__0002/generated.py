import json
from typing import Dict, Any

def process_json_input(req: Dict[str, Any]) -> Dict[str, Any]:
    """
    Parse the JSON body of a FastAPI request.

    Parameters
    ----------
    req : dict
        A dictionary representing the incoming HTTP request. It must contain
        at least two keys:
            - "headers": a mapping of header names to values.
            - "body": the raw request body as bytes or str.

    Returns
    -------
    dict
        The decoded JSON payload.

    Raises
    ------
    ValueError
        If the Content-Type header is missing or not ``application/json``.
        If the body cannot be decoded as valid JSON.
    """
    # Extract headers and body
    headers = req.get("headers", {})
    body = req.get("body")

    if body is None:
        raise ValueError("Request body is missing.")

    # Normalise header names to lowercase for case‑insensitive lookup
    content_type = headers.get("content-type") or headers.get("Content-Type")
    if not content_type:
        raise ValueError("Missing 'Content-Type' header.")

    # Ensure the Content‑Type is exactly application/json
    if content_type.split(";")[0].strip().lower() != "application/json":
        raise ValueError(
            f"Unsupported Content-Type: '{content_type}'. Expected 'application/json'."
        )

    # Decode body to string if it is bytes
    if isinstance(body, bytes):
        try:
            body_str = body.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise ValueError(f"Body is not valid UTF‑8: {exc}") from exc
    elif isinstance(body, str):
        body_str = body
    else:
        raise ValueError("Body must be bytes or str.")

    # Parse JSON safely
    try:
        payload = json.loads(body_str)
    except json.JSONDecodeError as exc:
        raise ValueError(f"Malformed JSON: {exc}") from exc

    if not isinstance(payload, dict):
        raise ValueError("JSON payload must be an object (dictionary).")

    return payload