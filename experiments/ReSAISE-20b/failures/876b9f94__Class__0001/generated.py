import json
from typing import Dict, Any


def process_json_input(req: Dict[str, Any]) -> Dict[str, Any]:
    """
    Parse and validate a JSON request body.

    Parameters
    ----------
    req : dict
        Dictionary containing the HTTP headers and body of the incoming request.
        Expected keys:
            - "headers": dict, may contain a "Content-Type" entry
            - "body": str or bytes containing the raw request payload

    Returns
    -------
    dict
        The decoded JSON object.

    Raises
    ------
    ValueError
        If the Content-Type is not application/json.
        If the body cannot be decoded as valid JSON.
    """
    # Ensure headers exist and are a dictionary
    if not isinstance(req.get("headers"), dict):
        raise ValueError("Request headers must be a dictionary.")

    # Retrieve and validate the Content-Type header
    content_type = req["headers"].get("Content-Type", "")
    # Normalise to lowercase for comparison
    if content_type.lower() != "application/json":
        raise ValueError(
            f"Unsupported Content-Type '{content_type}'. Expected 'application/json'."
        )

    # Retrieve the body
    body = req.get("body")
    if body is None:
        raise ValueError("Request body is missing.")
    if isinstance(body, bytes):
        try:
            body = body.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise ValueError("Body bytes could not be decoded as UTF-8.") from exc

    if not isinstance(body, str):
        raise ValueError("Request body must be a string or bytes.")

    # Attempt to parse the JSON
    try:
        parsed = json.loads(body)
    except json.JSONDecodeError as exc:
        raise ValueError(f"Malformed JSON: {exc.msg}") from exc

    if not isinstance(parsed, dict):
        raise ValueError("JSON payload must be an object (dictionary).")

    return parsed