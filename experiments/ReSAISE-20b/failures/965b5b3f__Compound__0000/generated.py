import json
from typing import Dict, Any


def process_json_request(req_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Parse and validate a JSON request body from FastAPI.

    Parameters
    ----------
    req_data : dict
        A dictionary containing the request headers and body.
        Expected keys are:
            * ``headers`` : mapping of header names to values
            * ``body``    : raw request body as bytes or str

    Returns
    -------
    dict
        The parsed JSON payload.

    Raises
    ------
    ValueError
        If the request does not contain a valid JSON body,
        if the content type is not acceptable, or
        if a CSRF token header is missing.
    """
    # 1. Validate the presence of headers and body
    if not isinstance(req_data, dict):
        raise ValueError("Request data must be a dictionary.")
    headers = req_data.get("headers")
    body = req_data.get("body")

    if headers is None or body is None:
        raise ValueError("Request data must contain 'headers' and 'body' keys.")

    # 2. Check the Content-Type header (case‑insensitive)
    content_type = None
    for key, value in headers.items():
        if key.lower() == "content-type":
            content_type = value
            break

    acceptable_types = {"application/json", "application/json; charset=utf-8"}
    if content_type not in acceptable_types:
        raise ValueError(
            f"Unsupported Content-Type: {content_type!r}. "
            "Expected 'application/json'."
        )

    # 3. CSRF protection: require an X-CSRF-Token header
    csrf_token = None
    for key, value in headers.items():
        if key.lower() == "x-csrf-token":
            csrf_token = value
            break

    if not csrf_token:
        raise ValueError("Missing CSRF token header 'X-CSRF-Token'.")

    # 4. Decode the body (bytes or str)
    if isinstance(body, bytes):
        try:
            body_text = body.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise ValueError("Request body is not valid UTF‑8.") from exc
    elif isinstance(body, str):
        body_text = body
    else:
        raise ValueError("Request body must be bytes or str.")

    # 5. Parse JSON
    try:
        payload = json.loads(body_text)
    except json.JSONDecodeError as exc:
        raise ValueError(f"Invalid JSON payload: {exc.msg}") from exc

    if not isinstance(payload, dict):
        raise ValueError("JSON payload must be an object (dict).")

    return payload