import json

def process_json_request(req_data: dict) -> dict:
    """
    Parse and validate the body of an incoming JSON request.

    Parameters
    ----------
    req_data : dict
        Dictionary containing the headers and body of the request.
        Expected keys:
            - 'headers': dict, HTTP request headers
            - 'body'   : bytes or str, raw body content

    Returns
    -------
    dict
        The parsed JSON object.

    Raises
    ------
    ValueError
        If the Content-Type header is missing or not `application/json`.
        If the body cannot be decoded as UTF‑8.
        If the JSON is malformed or not an object.
    """
    # Extract headers and body
    headers = req_data.get("headers", {})
    body = req_data.get("body")

    # Validate Content-Type header
    content_type = (
        headers.get("Content-Type") or headers.get("content-type") or ""
    ).strip()
    if not content_type:
        raise ValueError("Missing Content-Type header")

    # Strip parameters (e.g., charset) and compare
    mime_type = content_type.split(";")[0].strip().lower()
    if mime_type != "application/json":
        raise ValueError(f"Unsupported Content-Type: {content_type}")

    # Ensure body is bytes or str
    if isinstance(body, bytes):
        try:
            body_text = body.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise ValueError("Body is not valid UTF‑8") from exc
    elif isinstance(body, str):
        body_text = body
    else:
        raise ValueError("Body must be bytes or str")

    # Parse JSON safely
    try:
        parsed = json.loads(body_text)
    except json.JSONDecodeError as exc:
        raise ValueError(f"Invalid JSON: {exc.msg}") from exc

    # The API expects a JSON object (dict)
    if not isinstance(parsed, dict):
        raise ValueError("JSON body must be an object")

    return parsed