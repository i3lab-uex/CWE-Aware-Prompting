import json
from typing import Dict, Any


def validate_json_request(input_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Parse and validate the body of an incoming JSON request.

    Parameters
    ----------
    input_data : dict
        A dictionary containing at least the keys 'headers' and 'body'.
        ``input_data['headers']`` should be a mapping of header names to values.
        ``input_data['body']`` can be either a bytes object or a string.

    Returns
    -------
    dict
        The decoded JSON payload as a Python dictionary.

    Raises
    ------
    ValueError
        If the `Content-Type` header is missing or does not contain
        ``application/json``.
    ValueError
        If the body cannot be decoded as valid JSON or is not a dictionary.

    Notes
    -----
    * The function does **not** perform any further schema validation; it only
      ensures that the request claims to be JSON and can actually be decoded.
    * The check for ``application/json`` is case‑insensitive and accepts
      parameters such as ``charset=utf-8``.
    """
    # Extract headers safely; default to empty dict if missing
    headers = input_data.get("headers", {})
    content_type = headers.get("Content-Type") or headers.get("content-type")

    if not content_type:
        raise ValueError(
            "Missing 'Content-Type' header; expected 'application/json'."
        )

    # Accept content types that include application/json (e.g., with charset)
    if "application/json" not in content_type.lower():
        raise ValueError(
            f"Unsupported Content-Type '{content_type}'. Expected 'application/json'."
        )

    # Retrieve body; it may be bytes or str
    raw_body = input_data.get("body")
    if raw_body is None:
        raise ValueError("Missing request body.")

    # Decode bytes to str if necessary
    if isinstance(raw_body, bytes):
        try:
            raw_body = raw_body.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise ValueError(f"Body could not be decoded as UTF-8: {exc}") from exc

    if not isinstance(raw_body, str):
        raise ValueError(
            f"Unexpected body type {type(raw_body).__name__}; expected str or bytes."
        )

    # Parse JSON
    try:
        parsed = json.loads(raw_body)
    except json.JSONDecodeError as exc:
        raise ValueError(f"Invalid JSON payload: {exc}") from exc

    # Ensure the parsed payload is a dictionary
    if not isinstance(parsed, dict):
        raise ValueError(
            f"JSON payload must be an object (dict), got {type(parsed).__name__}."
        )

    return parsed