import json
from typing import Dict, Any

def validate_json_request(input_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Parse and validate a JSON request body.

    Parameters
    ----------
    input_data : dict
        Dictionary containing the incoming HTTP request data.
        Expected keys:
            - 'headers': Mapping of header names to values.
            - 'body': Raw request body as bytes or str.

    Returns
    -------
    dict
        The decoded JSON payload.

    Raises
    ------
    ValueError
        If the Content-Type header is missing or not a JSON media type.
        If the body cannot be decoded as valid JSON.

    Notes
    -----
    * The function performs a basic content‑type check to mitigate CWE-345.
      It accepts media types that start with ``application/json`` (e.g. 
      ``application/json; charset=utf-8``).  It does not attempt to verify
      cryptographic signatures, as that is beyond the scope of this helper.
    * The body size is limited to 10 MiB to prevent denial‑of‑service
      attacks. Adjust the limit as appropriate for your application.
    """
    # --- 1. Retrieve headers and body ---------------------------------------
    headers = input_data.get("headers", {})
    if not isinstance(headers, dict):
        raise ValueError("Headers must be a dictionary.")

    body = input_data.get("body")
    if body is None:
        raise ValueError("Missing request body.")
    # Accept bytes or string; convert to str if needed
    if isinstance(body, bytes):
        try:
            body = body.decode("utf-8")
        except Exception as exc:
            raise ValueError(f"Unable to decode request body: {exc}") from exc
    elif not isinstance(body, str):
        raise ValueError("Request body must be bytes or string.")

    # --- 2. Validate Content-Type ------------------------------------------
    content_type = headers.get("Content-Type") or headers.get("content-type")
    if not content_type:
        raise ValueError("Missing Content-Type header.")
    # Only accept application/json variants
    if not content_type.lower().startswith("application/json"):
        raise ValueError(
            f"Unsupported Content-Type '{content_type}'. Expected 'application/json'."
        )

    # --- 3. Limit body size (optional but recommended) ---------------------
    MAX_BODY_SIZE = 10 * 1024 * 1024  # 10 MiB
    if len(body.encode("utf-8")) > MAX_BODY_SIZE:
        raise ValueError(f"Request body exceeds {MAX_BODY_SIZE} bytes limit.")

    # --- 4. Parse JSON ------------------------------------------------------
    try:
        payload = json.loads(body)
    except json.JSONDecodeError as exc:
        raise ValueError(f"Invalid JSON payload: {exc}") from exc

    if not isinstance(payload, dict):
        raise ValueError("JSON payload must be an object (dictionary).")

    return payload