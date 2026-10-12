import json
from typing import Dict, Any


def process_json_input(req: Dict[str, Any]) -> Dict[str, Any]:
    """
    Parse the JSON body of a FastAPI request.

    Parameters
    ----------
    req : dict
        A dictionary containing the HTTP headers and body of the incoming request.
        Expected keys:
            - 'headers': a mapping of header names to values
            - 'body'   : the raw request body (str or bytes)

    Returns
    -------
    dict
        The decoded JSON object.

    Raises
    ------
    ValueError
        If the `Content-Type` header is missing or not set to 'application/json'.
        If the body cannot be decoded as valid JSON.
    """
    # --- 1. Validate Content-Type header ------------------------------------
    headers = req.get("headers", {})
    # Normalise header names to lowercase for case‑insensitive lookup
    content_type = next(
        (v for k, v in headers.items() if k.lower() == "content-type"),
        None,
    )
    if not content_type or "application/json" not in content_type.lower():
        raise ValueError(
            f"Unsupported Content-Type: {content_type!r}. Expected 'application/json'."
        )

    # --- 2. Retrieve and decode the body -------------------------------------
    raw_body = req.get("body")
    if raw_body is None:
        raise ValueError("Request body is missing.")

    # FastAPI may provide the body as bytes or str
    if isinstance(raw_body, bytes):
        try:
            raw_body = raw_body.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise ValueError(f"Body contains invalid UTF‑8 characters: {exc}") from exc

    if not isinstance(raw_body, str):
        raise ValueError(
            f"Body must be a string or bytes, got {type(raw_body).__name__}"
        )

    # --- 3. Parse JSON -------------------------------------------------------
    try:
        parsed = json.loads(raw_body)
    except json.JSONDecodeError as exc:
        raise ValueError(f"Malformed JSON: {exc}") from exc

    if not isinstance(parsed, dict):
        raise ValueError(
            f"JSON payload must be an object (dict), got {type(parsed).__name__}"
        )

    return parsed