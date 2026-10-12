import json
from typing import Any, Dict

# Define a reasonable maximum payload size (1 MB)
MAX_PAYLOAD_BYTES = 1 * 1024 * 1024
# Acceptable MIME types for JSON payloads
ACCEPTABLE_CONTENT_TYPES = {
    "application/json",
    "application/ld+json",
    "application/vnd.api+json",
}

def _get_header_value(headers: Dict[str, Any], key: str) -> str | None:
    """
    Retrieve a header value in a case‑insensitive manner.
    Returns None if the key is missing.
    """
    for hdr_key, value in headers.items():
        if hdr_key.lower() == key.lower():
            return str(value)
    return None


def validate_and_parse_json(incoming_req: Dict[str, Any]) -> Dict[str, Any]:
    """
    Validate that an incoming HTTP request contains a well‑formed JSON body
    and return the parsed dictionary.

    Parameters
    ----------
    incoming_req : dict
        Dictionary with two expected keys:
            - 'headers': mapping of header names to values.
            - 'body'   : the raw request body (bytes or str).

    Returns
    -------
    dict
        The parsed JSON payload.

    Raises
    ------
    ValueError
        If the Content‑Type header is missing or not a JSON MIME type,
        if the body cannot be decoded as UTF‑8, if the payload exceeds
        the configured size limit, or if JSON parsing fails.
    """
    # ---- Header validation -------------------------------------------------
    headers = incoming_req.get("headers")
    if not isinstance(headers, dict):
        raise ValueError("Request must contain a 'headers' dictionary.")

    content_type = _get_header_value(headers, "Content-Type")
    if not content_type:
        raise ValueError("Missing Content‑Type header.")
    # Normalize and check MIME type
    mime_type = content_type.split(";")[0].strip().lower()
    if mime_type not in ACCEPTABLE_CONTENT_TYPES:
        raise ValueError(
            f"Unsupported Content‑Type '{content_type}'. "
            "Only JSON content types are allowed."
        )

    # ---- Body validation ---------------------------------------------------
    body = incoming_req.get("body")
    if body is None:
        raise ValueError("Missing request body.")

    # Enforce payload size limit
    if isinstance(body, bytes):
        body_len = len(body)
    else:
        # If it's a string, encode to UTF‑8 for size check
        body_len = len(body.encode("utf-8"))

    if body_len > MAX_PAYLOAD_BYTES:
        raise ValueError(
            f"Payload size {body_len} bytes exceeds the maximum "
            f"allowed limit of {MAX_PAYLOAD_BYTES} bytes."
        )

    # Decode body to string if necessary
    try:
        if isinstance(body, bytes):
            body_str = body.decode("utf-8")
        else:
            body_str = str(body)
    except Exception as exc:  # pragma: no cover
        raise ValueError("Request body is not valid UTF‑8.") from exc

    # ---- JSON parsing -------------------------------------------------------
    try:
        parsed = json.loads(body_str)
    except json.JSONDecodeError as exc:  # pragma: no cover
        raise ValueError("Malformed JSON payload.") from exc

    if not isinstance(parsed, dict):
        # The API expects a JSON object (dictionary) at the top level.
        raise ValueError("JSON payload must be an object (dict).")

    return parsed