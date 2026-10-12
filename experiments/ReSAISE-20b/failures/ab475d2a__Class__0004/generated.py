import json
from typing import Dict, Any


def decode_json_request(req: Dict[str, Any]) -> Dict[str, Any]:
    """
    Parse and validate a JSON request body.

    Parameters
    ----------
    req : dict
        A dictionary containing at least the keys 'headers' and 'body'.
        `req['headers']` should be a mapping of HTTP header names to values.
        `req['body']` should be the raw request body, either as a string or
        bytes.

    Returns
    -------
    dict
        The decoded JSON object.

    Raises
    ------
    ValueError
        If the request Content-Type is not application/json (or a JSON media type)
        or if the body cannot be decoded as valid JSON.
    """
    # Ensure headers and body are present
    if not isinstance(req, dict):
        raise ValueError("Request must be a dictionary containing headers and body.")
    if "headers" not in req or "body" not in req:
        raise ValueError("Request dictionary must contain 'headers' and 'body' keys.")

    headers = req["headers"]
    body = req["body"]

    # Normalize header names to lower case for case‑insensitive comparison
    content_type = None
    if isinstance(headers, dict):
        for key, value in headers.items():
            if key.lower() == "content-type":
                content_type = str(value).lower()
                break
    else:
        raise ValueError("Headers must be a dictionary mapping header names to values.")

    # Accept only JSON media types
    if content_type is None or not (
        content_type.startswith("application/json")
        or content_type == "text/json"
    ):
        raise ValueError(
            f"Unsupported Content-Type '{content_type}'. Expected application/json."
        )

    # Decode body to string if it is bytes
    if isinstance(body, bytes):
        try:
            body_str = body.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise ValueError(f"Body bytes could not be decoded as UTF‑8: {exc}") from exc
    elif isinstance(body, str):
        body_str = body
    else:
        raise ValueError("Body must be a string or bytes.")

    # Attempt JSON parsing
    try:
        parsed = json.loads(body_str)
    except json.JSONDecodeError as exc:
        raise ValueError(f"Invalid JSON: {exc}") from exc

    if not isinstance(parsed, dict):
        raise ValueError("JSON payload must be an object (dictionary).")

    return parsed