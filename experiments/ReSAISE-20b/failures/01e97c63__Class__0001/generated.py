import json
from typing import Any, Dict


def handle_json_input(client_request: Dict[str, Any]) -> Dict:
    """
    Validate and parse a JSON HTTP request.

    Parameters
    ----------
    client_request : dict
        A dictionary containing the keys 'headers' and 'body'.
        * ``client_request['headers']`` must be a mapping (case‑insensitive).
        * ``client_request['body']`` is expected to be a string or bytes containing JSON.

    Returns
    -------
    dict
        The parsed JSON object.

    Raises
    ------
    ValueError
        If the Content‑Type header is missing or not a JSON‑compatible value.
        If the request body cannot be decoded as valid JSON.

    Notes
    -----
    * The function checks for common content‑type values such as
      ``application/json`` and ``application/*+json``.
    * It performs a case‑insensitive comparison of header names and values.
    * The body is decoded using UTF‑8 if it is bytes; otherwise the string
      is used directly.
    * This function does not perform authentication or origin checks,
      which are beyond its scope.  The caller should ensure the request
      originates from a trusted source if required.
    """
    # 1. Retrieve headers and body
    headers = client_request.get("headers", {})
    body = client_request.get("body")

    if not isinstance(headers, dict):
        raise ValueError("Headers must be a dictionary.")

    # 2. Normalize header names to lowercase for case‑insensitive lookup
    normalized_headers = {k.lower(): v for k, v in headers.items()}

    # 3. Verify Content‑Type
    content_type = normalized_headers.get("content-type")
    if not content_type:
        raise ValueError("Missing Content‑Type header.")

    # Accept common JSON media types
    json_media_types = (
        "application/json",
        "application/ld+json",
        "application/vnd.api+json",
    )
    if not any(
        ct.lower().startswith(mt) or f"+{mt.split('/')[-1]}" in ct.lower()
        for mt in json_media_types
    ):
        raise ValueError(f"Unsupported Content‑Type: {content_type}")

    # 4. Prepare body string
    if isinstance(body, bytes):
        try:
            body_str = body.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise ValueError("Body bytes could not be decoded as UTF‑8.") from exc
    elif isinstance(body, str):
        body_str = body
    else:
        raise ValueError("Body must be a string or bytes containing JSON.")

    # 5. Parse JSON
    try:
        parsed = json.loads(body_str)
    except json.JSONDecodeError as exc:
        raise ValueError("Malformed JSON in request body.") from exc

    # 6. Ensure the parsed object is a dictionary
    if not isinstance(parsed, dict):
        raise ValueError("JSON body must represent an object (dictionary).")

    return parsed