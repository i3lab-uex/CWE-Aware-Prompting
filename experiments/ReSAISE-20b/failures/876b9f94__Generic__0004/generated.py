import json
from typing import Any, Dict


def process_json_input(req: Dict[str, Any]) -> Dict[str, Any]:
    """
    Parse a JSON request body from a FastAPI-like request dictionary.

    Parameters
    ----------
    req : dict
        Dictionary containing the HTTP headers and body of the incoming request.
        Expected keys:
            - "headers": a mapping (dict) of HTTP header names to values.
            - "body": the raw request body, either a `str`, `bytes`, or already parsed
              dictionary.

    Returns
    -------
    dict
        The parsed JSON body as a Python dictionary.

    Raises
    ------
    ValueError
        If the `Content-Type` header is missing or not JSON, or if the body cannot be
        decoded as valid JSON.
    """
    # Grab headers and body, normalizing to dict for safety
    headers = req.get("headers", {})
    if not isinstance(headers, dict):
        raise ValueError("Request headers must be a dictionary")

    body = req.get("body")
    if body is None:
        raise ValueError("Request body is missing")

    # Validate Content-Type header
    content_type = headers.get("Content-Type") or headers.get("content-type")
    if not content_type:
        raise ValueError("Missing Content-Type header")

    # Accept application/json or any subtype like application/json; charset=utf-8
    if not content_type.lower().startswith("application/json"):
        raise ValueError(f"Unsupported Content-Type: {content_type}")

    # If body is already a dict, return it directly
    if isinstance(body, dict):
        return body

    # If body is bytes, decode to string using utf-8
    if isinstance(body, bytes):
        try:
            body = body.decode("utf-8")
        except Exception as exc:  # pragma: no cover
            raise ValueError("Failed to decode request body bytes as UTF-8") from exc

    # If body is a string, parse JSON
    if isinstance(body, str):
        try:
            parsed = json.loads(body)
        except json.JSONDecodeError as exc:  # pragma: no cover
            raise ValueError(f"Malformed JSON payload: {exc.msg}") from exc

        if not isinstance(parsed, dict):
            raise ValueError("JSON payload must be an object (dictionary)")

        return parsed

    # Unsupported body type
    raise ValueError(f"Unsupported request body type: {type(body).__name__}")