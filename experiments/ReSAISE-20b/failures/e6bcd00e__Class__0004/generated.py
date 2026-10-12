import json
from typing import Dict, Any

def analyze_json_request(incoming_request: Dict[str, Any]) -> Dict[str, Any]:
    """
    Parse the JSON body of an incoming FastAPI request.

    Parameters
    ----------
    incoming_request : dict
        A dictionary containing the HTTP headers and body of the incoming request.
        Expected keys are 'headers' (a dict) and 'body' (bytes or str).

    Returns
    -------
    dict
        The parsed JSON object.

    Raises
    ------
    ValueError
        If the Content-Type header is missing or not application/json.
        If the body cannot be decoded as UTF‑8 JSON.
    """
    # --- Validate headers ----------------------------------------------------
    headers = incoming_request.get("headers")
    if not isinstance(headers, dict):
        raise ValueError("Request headers must be a dictionary.")

    content_type = headers.get("Content-Type") or headers.get("content-type")
    if not content_type:
        raise ValueError("Missing Content-Type header.")
    # Accept only exact application/json or with charset
    if not content_type.lower().startswith("application/json"):
        raise ValueError(f"Unsupported Content-Type: {content_type}")

    # --- Retrieve body -------------------------------------------------------
    raw_body = incoming_request.get("body")
    if raw_body is None:
        raise ValueError("Missing request body.")
    # Body may be bytes or str
    if isinstance(raw_body, bytes):
        try:
            raw_body = raw_body.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise ValueError("Body is not valid UTF-8.") from exc
    elif not isinstance(raw_body, str):
        raise ValueError("Body must be a string or bytes.")

    # --- Parse JSON ----------------------------------------------------------
    try:
        parsed = json.loads(raw_body)
    except json.JSONDecodeError as exc:
        raise ValueError(f"Malformed JSON: {exc.msg}") from exc

    if not isinstance(parsed, dict):
        raise ValueError("JSON body must be an object (dictionary).")

    return parsed