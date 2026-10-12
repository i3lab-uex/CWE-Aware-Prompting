import json
from typing import Any, Dict

def decode_json_request(req: Dict[str, Any]) -> Dict[str, Any]:
    """
    Parse and validate a JSON request body.

    Parameters
    ----------
    req : dict
        A dictionary containing the keys ``headers`` and ``body``. The headers
        should be a mapping of header names to values (case‑insensitive), and
        the body should be either a ``bytes`` or ``str`` instance.

    Returns
    -------
    dict
        The decoded JSON object.

    Raises
    ------
    ValueError
        If the Content-Type is missing or not ``application/json``.
        If JSON decoding fails.
    """
    # ---- Verify content type ------------------------------------------------
    headers = req.get("headers", {})
    if not isinstance(headers, dict):
        raise ValueError("Request headers must be a dictionary.")

    # Normalise header names to lower case for comparison
    content_type = None
    for key, value in headers.items():
        if isinstance(key, str) and key.lower() == "content-type":
            content_type = value
            break

    if not content_type or "application/json" not in content_type.lower():
        raise ValueError("Unsupported Content-Type: must be application/json")

    # ---- Decode body --------------------------------------------------------
    body = req.get("body")
    if isinstance(body, bytes):
        try:
            body_str = body.decode("utf-8")
        except Exception as exc:  # pragma: no cover
            raise ValueError(f"Failed to decode request body bytes: {exc}") from exc
    elif isinstance(body, str):
        body_str = body
    else:
        raise ValueError("Request body must be bytes or str")

    try:
        decoded = json.loads(body_str)
    except json.JSONDecodeError as exc:
        raise ValueError(f"Invalid JSON payload: {exc}") from exc

    if not isinstance(decoded, dict):
        raise ValueError("JSON payload must be an object (dict)")

    return decoded