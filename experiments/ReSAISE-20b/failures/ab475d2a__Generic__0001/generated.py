import json
from typing import Dict, Any


def decode_json_request(req: Dict[str, Any]) -> Dict[str, Any]:
    """
    Parse and validate a JSON request body.

    Parameters
    ----------
    req : dict
        A dictionary containing at least the keys ``headers`` and ``body``.
        * ``req["headers"]`` must be a mapping of header names to values.
        * ``req["body"]`` can be either bytes or a str containing the raw request body.

    Returns
    -------
    dict
        The decoded JSON payload as a Python dictionary.

    Raises
    ------
    ValueError
        If the ``Content-Type`` header does not indicate JSON or if the body cannot be decoded.
    """
    # Basic sanity checks
    if not isinstance(req, dict):
        raise ValueError("Request must be a dictionary.")
    headers = req.get("headers", {})
    body = req.get("body")

    if not isinstance(headers, dict):
        raise ValueError("Headers must be a dictionary.")
    if body is None:
        raise ValueError("Request body is missing.")

    # Normalize header names to lowercase for case-insensitive comparison
    content_type = headers.get("Content-Type") or headers.get("content-type")
    if not isinstance(content_type, str) or "application/json" not in content_type.lower():
        raise ValueError("Unsupported Content-Type. Expected application/json.")

    # Ensure body is a string for json.loads
    if isinstance(body, bytes):
        try:
            body = body.decode("utf-8")
        except Exception as exc:  # pragma: no cover
            raise ValueError("Failed to decode request body bytes.") from exc

    if not isinstance(body, str):
        raise ValueError("Request body must be a string or bytes.")

    # Optionally enforce a maximum size (e.g., 1MB)
    MAX_BODY_SIZE = 1 * 1024 * 1024
    if len(body.encode("utf-8")) > MAX_BODY_SIZE:
        raise ValueError(f"Request body exceeds the maximum allowed size of {MAX_BODY_SIZE} bytes.")

    # Parse JSON
    try:
        data = json.loads(body)
    except json.JSONDecodeError as exc:  # pragma: no cover
        raise ValueError(f"Invalid JSON payload: {exc.msg}") from exc

    if not isinstance(data, dict):
        raise ValueError("JSON payload must be an object (dictionary).")

    return data