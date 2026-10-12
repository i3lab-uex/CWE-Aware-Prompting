import json
from typing import Dict, Any

def process_json_request(req_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Parse and validate a JSON request.

    Parameters
    ----------
    req_data : dict
        Dictionary containing at least two keys:
            - "headers": a mapping of request headers.
            - "body": the raw body bytes or string.

    Returns
    -------
    dict
        The decoded JSON payload as a dictionary.

    Raises
    ------
    ValueError
        If the Content-Type header is missing or not `application/json`
        (or a variant with charset), or if the body cannot be decoded as
        valid JSON.
    """
    # 1. Retrieve headers and ensure Content-Type is present
    headers = req_data.get("headers", {})
    if not isinstance(headers, dict):
        raise ValueError("Request headers must be a dictionary.")

    content_type = headers.get("Content-Type") or headers.get("content-type")
    if not content_type:
        raise ValueError("Missing Content-Type header.")

    # 2. Validate the Content-Type value
    acceptable = ["application/json"]
    if not any(content_type.lower().startswith(ct) for ct in acceptable):
        raise ValueError(
            f"Unsupported Content-Type: '{content_type}'. "
            "Only 'application/json' is accepted."
        )

    # 3. Retrieve the body and ensure it is bytes or string
    raw_body = req_data.get("body")
    if raw_body is None:
        raise ValueError("Request body is missing.")
    if isinstance(raw_body, bytes):
        try:
            raw_body = raw_body.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise ValueError("Body is not valid UTF-8 encoded JSON.") from exc
    elif not isinstance(raw_body, str):
        raise ValueError("Body must be a string or bytes.")

    # 4. Parse JSON safely
    try:
        parsed = json.loads(raw_body)
    except json.JSONDecodeError as exc:
        raise ValueError(f"Invalid JSON payload: {exc.msg}") from exc

    # 5. Ensure the parsed object is a dictionary (typical for FastAPI models)
    if not isinstance(parsed, dict):
        raise ValueError("JSON payload must be an object (dictionary).")

    return parsed