import json
from typing import Dict, Any

# Maximum body size (bytes) we will accept. Helps mitigate DoS attacks.
MAX_BODY_SIZE = 10 * 1024 * 1024  # 10 MB


def validate_and_parse_json(incoming_req: Dict[str, Any]) -> Dict[str, Any]:
    """
    Validate that an incoming HTTP request contains a JSON body and parse it.

    Parameters
    ----------
    incoming_req : dict
        Dictionary with two keys:
            - 'headers': Mapping of HTTP header names to values.
            - 'body'   : Raw request body (bytes or str).

    Returns
    -------
    dict
        Parsed JSON content.

    Raises
    ------
    ValueError
        If the request does not contain a JSON-compatible Content-Type,
        if the body is larger than :data:`MAX_BODY_SIZE`,
        or if the JSON payload cannot be parsed.
    """
    # Ensure headers are present
    headers = incoming_req.get("headers")
    if not isinstance(headers, dict):
        raise ValueError("Missing or invalid headers in request")

    # Normalize header names to lower-case for comparison
    content_type = next(
        (v for k, v in headers.items() if k.lower() == "content-type"),
        None,
    )
    if content_type is None:
        raise ValueError("Missing Content-Type header")

    # Accept common JSON MIME types
    json_mime_types = {
        "application/json",
        "application/ld+json",
        "application/vnd.api+json",
    }
    # Handle parameters like charset=utf-8
    mime_type = content_type.split(";")[0].strip().lower()
    if mime_type not in json_mime_types:
        raise ValueError(f"Unsupported Content-Type: {content_type}")

    # Retrieve the body
    body = incoming_req.get("body")
    if body is None:
        raise ValueError("Missing request body")

    # Ensure body size does not exceed limit
    if isinstance(body, bytes):
        body_len = len(body)
    else:
        body_len = len(str(body).encode("utf-8"))
    if body_len > MAX_BODY_SIZE:
        raise ValueError(f"Request body exceeds maximum allowed size of {MAX_BODY_SIZE} bytes")

    # Convert body to string if necessary
    if isinstance(body, bytes):
        try:
            body_str = body.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise ValueError("Request body contains invalid UTF-8") from exc
    else:
        body_str = str(body)

    # Parse JSON safely
    try:
        parsed = json.loads(body_str)
    except json.JSONDecodeError as exc:
        raise ValueError("Malformed JSON in request body") from exc

    if not isinstance(parsed, dict):
        raise ValueError("JSON payload must be an object (dict)")

    return parsed