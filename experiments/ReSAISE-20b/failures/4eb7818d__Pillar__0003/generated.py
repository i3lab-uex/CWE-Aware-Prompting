import json
from typing import Dict, Any


def parse_json_request(request: Dict[str, Any]) -> Dict[str, Any]:
    """
    Parse and validate a JSON request body.

    The function expects a dictionary representing the incoming HTTP
    request with at least two keys:
        - "headers": a mapping of header names to values
        - "body":   the raw request body, either as a string or bytes

    The function will:
        1. Verify that the "Content-Type" header is set to a JSON media type.
        2. Decode the body using UTF-8 (if bytes) and parse it with `json.loads`.
        3. Return the resulting dictionary.

    Parameters
    ----------
    request : dict
        The incoming request representation.

    Returns
    -------
    dict
        The parsed JSON body.

    Raises
    ------
    ValueError
        If the Content-Type is not a JSON media type.
        If JSON decoding fails.
        If any other problem occurs during processing.
    """
    # Basic input validation
    if not isinstance(request, dict):
        raise ValueError("Request must be a dictionary.")

    headers = request.get("headers", {})
    if not isinstance(headers, dict):
        raise ValueError("Request headers must be a dictionary.")

    # Normalise header names to lowercase for case‑insensitive comparison
    headers_lower = {k.lower(): v for k, v in headers.items()}

    content_type = headers_lower.get("content-type", "")
    if not any(ct in content_type.lower() for ct in ("application/json", "text/json")):
        raise ValueError("Unsupported Content-Type; expected application/json.")

    body = request.get("body")
    if body is None:
        raise ValueError("Request body is missing.")

    # Convert bytes to string if necessary
    if isinstance(body, bytes):
        try:
            body = body.decode("utf-8")
        except Exception as exc:  # pragma: no cover
            raise ValueError(f"Failed to decode request body as UTF-8: {exc}")

    if not isinstance(body, str):
        raise ValueError("Request body must be a string or bytes.")

    # Parse JSON safely
    try:
        parsed = json.loads(body)
    except json.JSONDecodeError as exc:
        raise ValueError(f"JSON decoding failed: {exc}") from exc
    except Exception as exc:  # pragma: no cover
        raise ValueError(f"Unexpected error while parsing JSON: {exc}") from exc

    if not isinstance(parsed, dict):
        raise ValueError("Parsed JSON must be an object (dictionary).")

    return parsed