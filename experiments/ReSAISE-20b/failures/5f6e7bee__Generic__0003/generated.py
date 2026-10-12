import json
from typing import Any, Dict


def handle_json_request(http_request: Dict[str, Any]) -> Dict[str, Any]:
    """
    Parse a JSON request body from a FastAPI-like HTTP request dictionary.

    Parameters
    ----------
    http_request : dict
        A dictionary that contains at least the keys 'headers' and 'body'.
        ``http_request['headers']`` should be a mapping of header names to values.
        ``http_request['body']`` can be either a str or bytes containing the raw JSON payload.

    Returns
    -------
    dict
        The decoded JSON object represented as a Python dictionary.

    Raises
    ------
    ValueError
        * If the 'Content-Type' header is missing or not set to 'application/json'.
        * If the body cannot be decoded as JSON (malformed JSON, non‑JSON content, etc.).
    """
    # ---- 1. Validate headers --------------------------------------------------
    headers = http_request.get("headers", {})
    if not isinstance(headers, dict):
        raise ValueError("Request headers must be a dictionary.")

    # Header names are case‑insensitive
    content_type = None
    for key, value in headers.items():
        if key.lower() == "content-type":
            content_type = value
            break

    if content_type is None:
        raise ValueError("Missing 'Content-Type' header.")
    # Accept application/json or application/json; charset=utf-8, etc.
    if not content_type.lower().startswith("application/json"):
        raise ValueError(
            f"Unsupported Content-Type '{content_type}'. Expected 'application/json'."
        )

    # ---- 2. Retrieve and normalize body --------------------------------------
    raw_body = http_request.get("body")
    if raw_body is None:
        raise ValueError("Request body is missing.")
    # FastAPI may provide the body as bytes; convert to str
    if isinstance(raw_body, bytes):
        try:
            raw_body = raw_body.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise ValueError("Body is not valid UTF‑8 encoded text.") from exc
    if not isinstance(raw_body, str):
        raise ValueError("Request body must be a string or bytes.")

    # ---- 3. Decode JSON ------------------------------------------------------
    try:
        parsed = json.loads(raw_body)
    except json.JSONDecodeError as exc:
        raise ValueError(f"Malformed JSON: {exc.msg}") from exc

    if not isinstance(parsed, dict):
        raise ValueError("JSON payload must be an object (dictionary).")

    return parsed