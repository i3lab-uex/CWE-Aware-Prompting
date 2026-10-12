import json
from typing import Dict, Any


def decode_json_request(req: Dict[str, Any]) -> Dict[str, Any]:
    """
    Parse and validate the body of an incoming JSON request.

    Parameters
    ----------
    req : dict
        A dictionary containing the keys 'headers' and 'body'.  The
        ``headers`` value should be a mapping of header names to values,
        and the ``body`` value should be bytes or str representing the
        request payload.

    Returns
    -------
    dict
        The decoded JSON data as a dictionary.

    Raises
    ------
    ValueError
        If the request's Content-Type is not acceptable.
        If the body cannot be decoded as valid JSON.
    """
    # 1. Verify that the request contains a Content-Type header
    headers = req.get("headers", {})
    if not isinstance(headers, dict):
        raise ValueError("Request headers must be a dictionary")

    content_type = headers.get("Content-Type") or headers.get("content-type")
    if not content_type:
        raise ValueError("Missing Content-Type header")

    # 2. Accept only JSON content types
    if not any(ct in content_type.lower() for ct in ("application/json", "application/ld+json")):
        raise ValueError(f"Unsupported Content-Type: {content_type}")

    # 3. Retrieve and decode the body
    body = req.get("body")
    if body is None:
        raise ValueError("Request body is missing")

    # Body may be bytes or str; convert to string if needed
    if isinstance(body, bytes):
        try:
            body_str = body.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise ValueError("Body contains invalid UTF‑8 bytes") from exc
    elif isinstance(body, str):
        body_str = body
    else:
        raise ValueError("Body must be bytes or str")

    # 4. Parse the JSON payload
    try:
        data = json.loads(body_str)
    except json.JSONDecodeError as exc:
        raise ValueError(f"Invalid JSON payload: {exc.msg}") from exc

    # 5. Ensure the top‑level is a dictionary
    if not isinstance(data, dict):
        raise ValueError("JSON payload must be an object (dict)")

    return data