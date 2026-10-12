import json
from typing import Any, Dict

def decode_json_request(req: Dict[str, Any]) -> Dict[str, Any]:
    """
    Parse and validate a JSON request body.

    Parameters
    ----------
    req : dict
        Dictionary containing the HTTP request data.  It must have a
        ``headers`` key mapping to a dict of header names (case‑insensitive)
        and a ``body`` key containing the raw request body as either
        ``bytes`` or ``str``.

    Returns
    -------
    dict
        The decoded JSON payload.

    Raises
    ------
    ValueError
        If the request content type is not `application/json`
        or if the body cannot be decoded as JSON.
    """
    # --- Validate content type ------------------------------------------------
    headers = req.get("headers", {})
    # Header names are case‑insensitive; normalise to lowercase
    content_type = headers.get("content-type") or headers.get("Content-Type")
    if not content_type:
        raise ValueError("Missing Content-Type header")

    # Accept only application/json (ignore charset and parameters)
    if not content_type.lower().startswith("application/json"):
        raise ValueError(
            f"Unsupported Content-Type: {content_type}. "
            "Only 'application/json' is accepted."
        )

    # --- Retrieve body --------------------------------------------------------
    raw_body = req.get("body")
    if raw_body is None:
        raise ValueError("Missing request body")

    # Convert bytes to string if necessary
    if isinstance(raw_body, bytes):
        try:
            raw_body = raw_body.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise ValueError("Body is not valid UTF‑8") from exc
    elif not isinstance(raw_body, str):
        raise ValueError("Body must be a string or bytes")

    # --- Decode JSON ----------------------------------------------------------
    try:
        data = json.loads(raw_body, strict=True)
    except json.JSONDecodeError as exc:
        raise ValueError(f"Invalid JSON payload: {exc.msg}") from exc

    # Ensure the result is a dictionary
    if not isinstance(data, dict):
        raise ValueError("JSON payload must be an object (dictionary)")

    return data