import json
from typing import Dict, Any

def process_json_request(req_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Parse and validate the body of an incoming JSON request.

    Parameters
    ----------
    req_data : dict
        Dictionary containing at least the keys 'headers' and 'body'.
        `req_data['headers']` should be a mapping of header names to values.
        `req_data['body']` should be the raw request payload (bytes or str).

    Returns
    -------
    dict
        The decoded JSON payload as a Python dictionary.

    Raises
    ------
    ValueError
        If the Content-Type header is missing or not application/json.
        If the body cannot be decoded as valid JSON.
    """
    # ------------------------------------------------------------------
    # 1. Content‑type validation
    # ------------------------------------------------------------------
    headers = req_data.get("headers", {})
    if not isinstance(headers, dict):
        raise ValueError("Request headers must be a dictionary.")

    # Header names are case‑insensitive in HTTP
    content_type = next(
        (v for k, v in headers.items() if k.lower() == "content-type"), None
    )
    if content_type is None:
        raise ValueError("Missing Content-Type header.")
    # Allow charset parameter e.g. application/json; charset=utf-8
    if not content_type.lower().startswith("application/json"):
        raise ValueError(
            f"Unsupported Content-Type: {content_type!r}. Expected application/json."
        )

    # ------------------------------------------------------------------
    # 2. Body extraction
    # ------------------------------------------------------------------
    body = req_data.get("body")
    if body is None:
        raise ValueError("Missing request body.")
    # FastAPI may provide bytes or str; convert to str if needed
    if isinstance(body, bytes):
        try:
            body = body.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise ValueError("Request body is not valid UTF‑8.") from exc
    elif not isinstance(body, str):
        raise ValueError("Request body must be a string or bytes.")

    # ------------------------------------------------------------------
    # 3. JSON decoding
    # ------------------------------------------------------------------
    try:
        payload = json.loads(body)
    except json.JSONDecodeError as exc:
        raise ValueError(f"Invalid JSON payload: {exc.msg}") from exc

    if not isinstance(payload, dict):
        raise ValueError("JSON payload must be an object (dictionary).")

    # ------------------------------------------------------------------
    # 4. CSRF safety note
    # ------------------------------------------------------------------
    # The function itself does not perform CSRF checks.  In a real FastAPI
    # application you should guard endpoints with dependency injection that
    # verifies a CSRF token (e.g., `Depends(csrf_token_required)`).
    #
    # Returning the parsed payload is safe as long as you do not expose it
    # to unauthenticated users or store it in a place where XSS can read it.
    #
    # ------------------------------------------------------------------
    return payload