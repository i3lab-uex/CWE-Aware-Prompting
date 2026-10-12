import json
from typing import Dict, Any

def process_json_request(req_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Parse and validate the body of an incoming JSON request.

    Parameters
    ----------
    req_data : dict
        A dictionary containing at least the keys ``headers`` and ``body``.
        ``headers`` should be a mapping of HTTP header names to values
        (case‑insensitive). ``body`` should be the raw request body as a
        bytes-like object or str.

    Returns
    -------
    dict
        The parsed JSON payload as a Python dictionary.

    Raises
    ------
    ValueError
        If the request does not contain a Content-Type header that
        indicates JSON, or if the body cannot be decoded as valid JSON.
    """
    # Ensure headers exist and are a mapping
    if not isinstance(req_data, dict):
        raise ValueError("Request data must be a dictionary")

    headers = req_data.get("headers")
    if not isinstance(headers, dict):
        raise ValueError("Request headers must be a dictionary")

    # Normalise header names to lower case for case‑insensitive lookup
    content_type = next(
        (v for k, v in headers.items() if k.lower() == "content-type"),
        None,
    )
    if content_type is None:
        raise ValueError("Missing Content-Type header")

    # Accept only JSON media types
    if not content_type.lower().startswith("application/json"):
        raise ValueError(
            f"Unsupported Content-Type: {content_type}. "
            "Only application/json is accepted."
        )

    # Retrieve the body
    body = req_data.get("body")
    if body is None:
        raise ValueError("Missing request body")

    # Convert bytes to str if necessary
    if isinstance(body, (bytes, bytearray)):
        try:
            body_str = body.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise ValueError("Body is not valid UTF-8 encoded") from exc
    elif isinstance(body, str):
        body_str = body
    else:
        raise ValueError("Body must be a string or bytes")

    # Parse JSON
    try:
        parsed = json.loads(body_str)
    except json.JSONDecodeError as exc:
        raise ValueError(f"Invalid JSON payload: {exc.msg}") from exc

    if not isinstance(parsed, dict):
        raise ValueError("JSON payload must be an object (dict)")

    return parsed