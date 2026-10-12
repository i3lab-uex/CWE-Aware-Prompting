import json
from typing import Dict, Any


def validate_and_parse_json(incoming_req: Dict[str, Any]) -> Dict[str, Any]:
    """
    Validate the content type and parse a JSON request body.

    Parameters
    ----------
    incoming_req : dict
        A dictionary that contains at least the keys 'headers' and 'body'.
        The 'headers' value must be a mapping of header names to values
        (case‑insensitive). The 'body' value is the raw request body as a string.

    Returns
    -------
    dict
        The parsed JSON object from the request body.

    Raises
    ------
    ValueError
        If the content type is not JSON‑compatible,
        if the request body is not valid JSON,
        or if a CSRF token header is missing (simple protection against
        Cross‑Site Request Forgery attacks).
    """
    # Extract headers and body
    try:
        headers = incoming_req["headers"]
        raw_body = incoming_req["body"]
    except KeyError as exc:
        raise ValueError("Request must contain 'headers' and 'body'") from exc

    # Normalise header names to lower case for comparison
    headers_lower = {k.lower(): v for k, v in headers.items()}

    # 1. Verify Content‑Type header
    content_type = headers_lower.get("content-type", "")
    if "application/json" not in content_type.lower():
        raise ValueError(
            f"Unsupported Content-Type '{content_type}'. Expected 'application/json'."
        )

    # 2. Simple CSRF protection: require a custom header
    if "x-csrf-token" not in headers_lower:
        raise ValueError("Missing CSRF token header 'X-CSRF-Token'.")

    # 3. Parse the JSON body
    try:
        parsed_body = json.loads(raw_body)
    except (TypeError, json.JSONDecodeError) as exc:
        raise ValueError("Malformed JSON in request body.") from exc

    # 4. Ensure the parsed object is a dictionary
    if not isinstance(parsed_body, dict):
        raise ValueError("JSON payload must be an object (dictionary).")

    return parsed_body