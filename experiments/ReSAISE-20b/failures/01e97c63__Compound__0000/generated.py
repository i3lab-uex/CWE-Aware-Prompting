# fastapi_json_handler.py

import json
from typing import Dict, Any

class JsonRequestError(ValueError):
    """Custom exception for JSON request validation errors."""
    pass


def handle_json_input(client_request: Dict[str, Any]) -> Dict[str, Any]:
    """
    Validate and parse a JSON request.

    Parameters
    ----------
    client_request : dict
        A dictionary that must contain:
            - 'headers' (dict): HTTP request headers.
            - 'body'    (bytes or str): Raw request body.

    Returns
    -------
    dict
        The parsed JSON payload.

    Raises
    ------
    JsonRequestError
        If the content type is not JSON-compatible or if the body cannot be parsed as JSON.
    """
    # --- 1. Validate headers presence ---
    if not isinstance(client_request, dict):
        raise JsonRequestError("client_request must be a dictionary")

    headers = client_request.get("headers")
    if not isinstance(headers, dict):
        raise JsonRequestError("Missing or invalid 'headers' field in client_request")

    # --- 2. Check Content-Type header for JSON compatibility ---
    content_type = headers.get("Content-Type") or headers.get("content-type")
    if not content_type:
        raise JsonRequestError("Content-Type header is missing")

    # Accept common JSON MIME types
    json_mime_types = {
        "application/json",
        "application/json; charset=utf-8",
        "application/json;charset=utf-8",
    }
    # Normalize header value
    ct = content_type.split(";")[0].strip().lower()
    if ct not in {"application/json"}:
        raise JsonRequestError(f"Unsupported Content-Type: {content_type}")

    # --- 3. Retrieve and decode body ---
    raw_body = client_request.get("body")
    if raw_body is None:
        raise JsonRequestError("Missing request body")

    # FastAPI typically provides a bytes object; if str, use directly
    if isinstance(raw_body, bytes):
        try:
            body_text = raw_body.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise JsonRequestError("Body is not valid UTF-8") from exc
    elif isinstance(raw_body, str):
        body_text = raw_body
    else:
        raise JsonRequestError("Body must be bytes or str")

    # --- 4. Parse JSON ---
    try:
        payload = json.loads(body_text)
    except json.JSONDecodeError as exc:
        raise JsonRequestError("Malformed JSON payload") from exc

    if not isinstance(payload, dict):
        raise JsonRequestError("JSON payload must be an object (dict)")

    # --- 5. Optional CSRF protection hint ---
    # A real application should verify a CSRF token or same‑site cookie.
    csrf_token = headers.get("X-CSRF-Token") or headers.get("x-csrf-token")
    if csrf_token is None:
        # In a real system, you might raise an error or log a warning.
        pass  # Placeholder: CSRF validation is framework‑dependent.

    return payload