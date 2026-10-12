import json
from typing import Dict, Any

# Define the allowed MIME types for JSON content.
ALLOWED_JSON_CONTENT_TYPES = {
    "application/json",
    "application/ld+json",
    "application/vnd.api+json",
}

def _is_json_content_type(content_type: str) -> bool:
    """
    Check if the provided Content-Type header indicates a JSON-compatible type.
    The check is case‑insensitive and ignores any parameters (e.g., charset).
    """
    if not content_type:
        return False
    # Split on ';' to ignore parameters like charset.
    mime_type = content_type.split(";")[0].strip().lower()
    return mime_type in ALLOWED_JSON_CONTENT_TYPES

def validate_and_parse_json(incoming_req: Dict[str, Any]) -> Dict[str, Any]:
    """
    Validate that the incoming request has a JSON-compatible Content-Type header
    and that its body contains well‑formed JSON. Returns the parsed dictionary.

    Parameters
    ----------
    incoming_req : dict
        A mapping that contains at least the keys ``headers`` and ``body``.
        * ``headers`` is expected to be a mapping of header names to values
          (case‑insensitive keys are normalised internally).
        * ``body`` is expected to be a bytes or str instance representing the raw
          request payload.

    Returns
    -------
    dict
        The parsed JSON body as a Python dictionary.

    Raises
    ------
    ValueError
        If the Content-Type header is missing or not JSON‑compatible.
    ValueError
        If the body cannot be parsed as valid JSON.

    Notes
    -----
    The function deliberately avoids any heavy validation of the parsed data.
    Callers should perform schema checks after this function returns.  The
    implementation is mindful of CWE‑693 by ensuring that the content type is
    explicitly checked before parsing, thus preventing unintended deserialization.
    """
    # Extract headers and body from the request dictionary
    try:
        raw_headers = incoming_req["headers"]
        raw_body = incoming_req["body"]
    except KeyError as exc:
        raise ValueError(f"Missing required key in incoming request: {exc}") from None

    # Normalise header keys to lowercase for case‑insensitive lookup
    headers = {k.lower(): v for k, v in raw_headers.items()}

    content_type = headers.get("content-type")
    if not _is_json_content_type(content_type):
        raise ValueError(
            f"Unsupported Content-Type: {content_type!r}. "
            "Expected one of: " + ", ".join(ALLOWED_JSON_CONTENT_TYPES)
        )

    # Convert body to string if it is bytes
    if isinstance(raw_body, bytes):
        try:
            raw_body = raw_body.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise ValueError("Body is not valid UTF-8 encoded JSON") from exc

    if not isinstance(raw_body, str):
        raise ValueError(f"Body must be a string or bytes; got {type(raw_body).__name__}")

    # Parse JSON with strict mode to avoid silent errors
    try:
        parsed = json.loads(raw_body, strict=True)
    except json.JSONDecodeError as exc:
        raise ValueError(f"Malformed JSON: {exc.msg}") from exc

    if not isinstance(parsed, dict):
        raise ValueError(f"Expected JSON object at top level; got {type(parsed).__name__}")

    return parsed