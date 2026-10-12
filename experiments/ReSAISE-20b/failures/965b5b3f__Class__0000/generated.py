import json
from typing import Dict, Any

def process_json_request(req_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Parse and validate the body of an incoming JSON request.

    Parameters
    ----------
    req_data : dict
        Dictionary containing at least the keys ``headers`` and ``body``.
        * ``req_data['headers']`` should be a mapping of header names to values
          (case‑insensitive).  The function looks for ``Content-Type``.
        * ``req_data['body']`` should be a bytes object or a str containing
          the raw request body.

    Returns
    -------
    dict
        The decoded JSON payload.

    Raises
    ------
    ValueError
        If the request is not marked as JSON (content type mismatch) or if the
        body cannot be decoded as valid JSON.
    """
    # ---- Header validation --------------------------------------------------
    headers = req_data.get("headers", {})
    if not isinstance(headers, dict):
        raise ValueError("Headers must be a dictionary")

    # Header names are case‑insensitive; normalise to lowercase
    content_type = None
    for key, value in headers.items():
        if isinstance(key, str) and key.lower() == "content-type":
            content_type = value
            break

    if not content_type or not content_type.lower().startswith("application/json"):
        raise ValueError(
            "Unsupported content type: expected 'application/json', got "
            f"'{content_type}'"
        )

    # ---- Body extraction ----------------------------------------------------
    body = req_data.get("body")
    if body is None:
        raise ValueError("Missing request body")

    # Ensure we have a str to feed json.loads
    if isinstance(body, bytes):
        try:
            body_text = body.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise ValueError(f"Body is not valid UTF-8: {exc}") from exc
    elif isinstance(body, str):
        body_text = body
    else:
        raise ValueError("Body must be bytes or str")

    # ---- JSON decoding ------------------------------------------------------
    try:
        parsed = json.loads(body_text)
    except json.JSONDecodeError as exc:
        raise ValueError(f"Invalid JSON payload: {exc}") from exc

    if not isinstance(parsed, dict):
        raise ValueError("JSON payload must be an object (dict)")

    return parsed