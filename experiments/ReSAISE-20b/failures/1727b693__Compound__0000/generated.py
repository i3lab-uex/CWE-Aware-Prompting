import json
from typing import Dict, Any


def validate_json_request(input_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Parse and validate the body of an incoming JSON request.

    Parameters
    ----------
    input_data : dict
        Dictionary containing at least the keys ``headers`` and ``body``.
        * ``headers`` must be a mapping of header names to values
          (case‑insensitive keys are accepted).
        * ``body`` is the raw request payload as a bytes object or string.

    Returns
    -------
    dict
        The decoded JSON body.

    Raises
    ------
    ValueError
        If the content type is not ``application/json`` or a related MIME type.
    ValueError
        If the request does not contain an ``X-CSRF-Token`` header.
    ValueError
        If the body cannot be decoded as valid JSON or is not a mapping.

    Notes
    -----
    * The function checks for the presence of an ``X-CSRF-Token`` header
      to mitigate CSRF attacks.  In a real application this token should be
      validated against a session or database value; here we simply ensure
      the header exists.
    * Header names are compared in a case‑insensitive manner.
    """
    # --- Validate headers ---------------------------------------------------
    if not isinstance(input_data, dict):
        raise ValueError("input_data must be a dictionary")

    headers = input_data.get("headers", {})
    if not isinstance(headers, dict):
        raise ValueError("'headers' must be a dictionary")

    # Normalise header names to lower case for easy lookup
    headers_lc = {k.lower(): v for k, v in headers.items()}

    # Content‑Type check
    content_type = headers_lc.get("content-type", "")
    if not any(ct in content_type.lower() for ct in ("application/json", "text/json")):
        raise ValueError(
            f"Unsupported Content-Type '{content_type}'. Expected application/json."
        )

    # CSRF token presence check (basic mitigation)
    if "x-csrf-token" not in headers_lc:
        raise ValueError("Missing X-CSRF-Token header (possible CSRF attack).")

    # --- Parse body ---------------------------------------------------------
    raw_body = input_data.get("body")
    if raw_body is None:
        raise ValueError("Request body is missing.")

    # Convert bytes to str if necessary
    if isinstance(raw_body, bytes):
        try:
            raw_body = raw_body.decode("utf-8")
        except Exception as exc:  # pragma: no cover
            raise ValueError("Failed to decode request body as UTF‑8.") from exc

    if not isinstance(raw_body, str):
        raise ValueError("Request body must be a string or bytes object.")

    try:
        parsed = json.loads(raw_body)
    except json.JSONDecodeError as exc:
        raise ValueError(f"Invalid JSON payload: {exc.msg}") from exc

    if not isinstance(parsed, dict):
        raise ValueError("JSON payload must be an object (dictionary).")

    return parsed