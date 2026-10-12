import json
from typing import Dict, Any


def process_json_input(req: Dict[str, Any]) -> Dict[str, Any]:
    """
    Parse the JSON body of an HTTP request.

    Parameters
    ----------
    req : dict
        A dictionary containing the request headers under the key ``"headers"``
        and the raw body under the key ``"body"``.  The body is expected to be a
        bytes-like object or a string.

    Returns
    -------
    dict
        The parsed JSON payload as a dictionary.

    Raises
    ------
    ValueError
        If the `Content-Type` header is missing or not set to a JSON media type,
        or if the body cannot be decoded as valid JSON.
    """
    # ------------------------------------------------------------------
    # 1. Validate the presence of headers and body
    # ------------------------------------------------------------------
    if not isinstance(req, dict):
        raise ValueError("Request must be a dictionary containing headers and body.")
    headers = req.get("headers", {})
    if not isinstance(headers, dict):
        raise ValueError("Request headers must be a dictionary.")
    body = req.get("body")
    if body is None:
        raise ValueError("Request body missing.")

    # ------------------------------------------------------------------
    # 2. Check Content-Type header for JSON
    # ------------------------------------------------------------------
    content_type = headers.get("Content-Type") or headers.get("content-type")
    if not content_type:
        raise ValueError("Missing 'Content-Type' header.")
    # Accept media types that start with application/json
    if not content_type.lower().startswith("application/json"):
        raise ValueError(
            f"Unsupported Content-Type '{content_type}'. Expected 'application/json'."
        )

    # ------------------------------------------------------------------
    # 3. Decode the body into a string if necessary
    # ------------------------------------------------------------------
    if isinstance(body, bytes):
        try:
            body_str = body.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise ValueError("Request body is not valid UTF-8.") from exc
    elif isinstance(body, str):
        body_str = body
    else:
        raise ValueError("Request body must be a string or bytes object.")

    # ------------------------------------------------------------------
    # 4. Parse JSON with strict validation
    # ------------------------------------------------------------------
    try:
        payload = json.loads(body_str, strict=True)
    except json.JSONDecodeError as exc:
        raise ValueError(f"Malformed JSON: {exc.msg}") from exc

    # ------------------------------------------------------------------
    # 5. Ensure the payload is a dictionary (typical for request bodies)
    # ------------------------------------------------------------------
    if not isinstance(payload, dict):
        raise ValueError("JSON payload must be an object (dictionary).")

    return payload