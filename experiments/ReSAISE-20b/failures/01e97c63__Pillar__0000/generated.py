import json
from typing import Dict

# Maximum allowed size for the request body (bytes) – helps mitigate denial‑of‑service attacks
MAX_BODY_SIZE = 2 ** 20  # 1 MiB


def handle_json_input(client_request: Dict) -> Dict:
    """
    Validate and parse the JSON body of an HTTP request.

    Parameters
    ----------
    client_request : dict
        Dictionary containing at least the keys 'headers' (dict) and 'body'
        (bytes or str).  The headers dictionary should be case‑insensitive
        for the 'Content-Type' key.

    Returns
    -------
    dict
        The parsed JSON object.

    Raises
    ------
    ValueError
        If the Content-Type header is missing or not a JSON‑compatible value.
    ValueError
        If the body is not valid JSON or exceeds ``MAX_BODY_SIZE`` bytes.
    """
    # ------------------------------------------------------------------
    # 1. Verify that the request contains headers and a body
    # ------------------------------------------------------------------
    if not isinstance(client_request, dict):
        raise ValueError("client_request must be a dictionary")

    headers = client_request.get("headers")
    if not isinstance(headers, dict):
        raise ValueError("Headers must be a dictionary")

    body = client_request.get("body")
    if body is None:
        raise ValueError("Missing request body")

    # ------------------------------------------------------------------
    # 2. Validate Content-Type header
    # ------------------------------------------------------------------
    # Header names are case‑insensitive; normalise to lower case.
    content_type = None
    for key, value in headers.items():
        if key.lower() == "content-type":
            content_type = str(value).lower()
            break

    if content_type is None:
        raise ValueError("Missing Content-Type header")

    # Accept common JSON MIME types
    if not any(ct in content_type for ct in ("application/json", "application/ld+json")):
        raise ValueError(f"Unsupported Content-Type: {content_type}")

    # ------------------------------------------------------------------
    # 3. Ensure body size is within limits
    # ------------------------------------------------------------------
    if isinstance(body, bytes):
        body_length = len(body)
        decoded_body = body.decode("utf-8")
    elif isinstance(body, str):
        body_length = len(body.encode("utf-8"))
        decoded_body = body
    else:
        raise ValueError("Body must be bytes or str")

    if body_length > MAX_BODY_SIZE:
        raise ValueError(f"Request body too large ({body_length} bytes)")

    # ------------------------------------------------------------------
    # 4. Parse JSON safely
    # ------------------------------------------------------------------
    try:
        parsed = json.loads(decoded_body)
    except json.JSONDecodeError as exc:
        raise ValueError(f"Malformed JSON: {exc}") from None

    if not isinstance(parsed, dict):
        raise ValueError("JSON body must be an object (dictionary)")

    # ------------------------------------------------------------------
    # 5. Return parsed content
    # ------------------------------------------------------------------
    return parsed