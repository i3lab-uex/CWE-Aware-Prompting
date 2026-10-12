import json
from typing import Dict, Any

def process_json_request(req_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Parse and validate a JSON request body.

    Parameters
    ----------
    req_data : dict
        A dictionary containing at least the keys ``headers`` and ``body``,
        where ``headers`` is a mapping of request headers (case‑insensitive)
        and ``body`` is the raw request payload as a bytes or string object.

    Returns
    -------
    dict
        The decoded JSON payload.

    Raises
    ------
    ValueError
        If the content type is not `application/json` or if JSON decoding fails.
    """
    # ---- Validate content type -------------------------------------------------
    headers = req_data.get("headers", {})
    if not isinstance(headers, dict):
        raise ValueError("Request headers must be a dictionary.")

    # Normalize header names to lower case for comparison
    content_type = None
    for key, value in headers.items():
        if key.lower() == "content-type":
            content_type = str(value).lower()
            break

    if not content_type or "application/json" not in content_type:
        raise ValueError(
            f"Unsupported Content-Type: {content_type or 'missing'}. "
            "Only application/json is accepted."
        )

    # ---- Decode JSON body -------------------------------------------------------
    raw_body = req_data.get("body", None)
    if raw_body is None:
        raise ValueError("Request body is missing.")

    # Ensure we have a string for json.loads
    if isinstance(raw_body, bytes):
        try:
            raw_body = raw_body.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise ValueError("Request body is not valid UTF‑8.") from exc

    if not isinstance(raw_body, str):
        raise ValueError("Request body must be a string or bytes.")

    try:
        payload = json.loads(raw_body)
    except json.JSONDecodeError as exc:
        raise ValueError(f"Invalid JSON payload: {exc.msg}") from exc

    if not isinstance(payload, dict):
        raise ValueError("JSON payload must be an object (dict).")

    return payload