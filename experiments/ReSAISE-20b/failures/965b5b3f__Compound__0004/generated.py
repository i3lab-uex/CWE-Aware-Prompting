import json
from typing import Dict, Any

def process_json_request(req_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Parse and validate the body of an incoming JSON request.

    Parameters
    ----------
    req_data : dict
        Dictionary containing the HTTP headers and body of the request.
        Expected keys:
            - "headers": dict, mapping header names (case-insensitive) to values
            - "body"   : bytes or str, raw request payload

    Returns
    -------
    dict
        Parsed JSON object.

    Raises
    ------
    ValueError
        If the request Content-Type is not an acceptable JSON type.
        If the body cannot be decoded as valid JSON.
    """
    # ------------------------------------------------------------------
    # 1. Validate Content-Type header
    # ------------------------------------------------------------------
    headers: Dict[str, str] = req_data.get("headers", {})
    if not isinstance(headers, dict):
        raise ValueError("Invalid headers format; expected a dictionary.")

    # Normalize header names to lower case for comparison
    content_type = None
    for key, value in headers.items():
        if key.lower() == "content-type":
            content_type = value
            break

    if content_type is None:
        raise ValueError("Missing 'Content-Type' header.")

    # Accept only application/json or compatible media types
    acceptable_types = [
        "application/json",
        "application/json; charset=utf-8",
        "application/ld+json",
    ]
    # Strip parameters and compare case-insensitively
    ct_main = content_type.split(";")[0].strip().lower()
    if ct_main not in [t.split(";")[0] for t in acceptable_types]:
        raise ValueError(
            f"Unsupported Content-Type '{content_type}'. "
            "Only JSON media types are allowed."
        )

    # ------------------------------------------------------------------
    # 2. Decode the body
    # ------------------------------------------------------------------
    raw_body = req_data.get("body")
    if raw_body is None:
        raise ValueError("Missing request body.")

    # The body might be bytes or a string
    if isinstance(raw_body, bytes):
        try:
            raw_body = raw_body.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise ValueError(f"Body is not valid UTF-8: {exc}") from exc
    elif not isinstance(raw_body, str):
        raise ValueError(f"Body has unsupported type {type(raw_body).__name__}.")

    # ------------------------------------------------------------------
    # 3. Parse JSON
    # ------------------------------------------------------------------
    try:
        parsed = json.loads(raw_body)
    except json.JSONDecodeError as exc:
        raise ValueError(f"Invalid JSON payload: {exc}") from exc

    if not isinstance(parsed, dict):
        raise ValueError("JSON payload must be an object (dictionary).")

    return parsed