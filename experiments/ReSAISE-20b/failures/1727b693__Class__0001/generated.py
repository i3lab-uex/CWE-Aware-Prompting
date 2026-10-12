import json
from typing import Any, Dict

def validate_json_request(input_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Validate and parse the body of an incoming JSON request.

    Parameters
    ----------
    input_data : dict
        A dictionary containing at least the keys 'headers' and 'body'.
        `input_data['headers']` should be a mapping of header names to values.
        `input_data['body']` should be a bytes-like object or str containing the raw
        request payload.

    Returns
    -------
    dict
        The parsed JSON payload as a dictionary.

    Raises
    ------
    ValueError
        If the request does not contain an acceptable content‑type header.
        If the body cannot be decoded as valid JSON.
    """
    # ------------------------------------------------------------------
    # 1. Validate presence of headers and body
    # ------------------------------------------------------------------
    if not isinstance(input_data, dict):
        raise ValueError("Input data must be a dictionary containing 'headers' and 'body'.")
    headers = input_data.get("headers", {})
    body = input_data.get("body")

    if not isinstance(headers, dict):
        raise ValueError("'headers' must be a dictionary.")
    if body is None:
        raise ValueError("Missing request body.")

    # ------------------------------------------------------------------
    # 2. Verify content‑type header
    # ------------------------------------------------------------------
    # Extract the first Content-Type header value (case-insensitive)
    content_type = None
    for key, value in headers.items():
        if key.lower() == "content-type":
            content_type = value
            break

    if not content_type or not isinstance(content_type, str):
        raise ValueError("Missing or invalid 'Content-Type' header.")

    # Accept only application/json; strip any parameters (e.g., charset)
    if not content_type.lower().startswith("application/json"):
        raise ValueError(
            f"Unsupported Content-Type '{content_type}'. Expected 'application/json'."
        )

    # ------------------------------------------------------------------
    # 3. Decode body
    # ------------------------------------------------------------------
    # If the body is bytes, decode using UTF-8; otherwise assume str.
    if isinstance(body, bytes):
        try:
            body_text = body.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise ValueError(f"Body contains invalid UTF-8: {exc}") from exc
    elif isinstance(body, str):
        body_text = body
    else:
        raise ValueError("Request body must be bytes or str.")

    # ------------------------------------------------------------------
    # 4. Parse JSON
    # ------------------------------------------------------------------
    try:
        parsed = json.loads(body_text)
    except json.JSONDecodeError as exc:
        raise ValueError(f"Invalid JSON payload: {exc}") from exc

    if not isinstance(parsed, dict):
        # For stricter validation we could allow lists, but the spec expects a dict
        raise ValueError("JSON payload must be an object (dict).")

    # ------------------------------------------------------------------
    # 5. Return the parsed payload
    # ------------------------------------------------------------------
    return parsed