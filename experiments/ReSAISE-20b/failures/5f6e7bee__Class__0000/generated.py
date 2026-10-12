import json
from typing import Dict, Any


def handle_json_request(http_request: Dict[str, Any]) -> Dict[str, Any]:
    """
    Parse a JSON request body from an HTTP request dictionary.

    Parameters
    ----------
    http_request : dict
        A dictionary representing the incoming HTTP request. It should contain:
            - 'headers': a mapping of header names to values.
            - 'body'   : the raw request body (str or bytes).

    Returns
    -------
    dict
        The parsed JSON object.

    Raises
    ------
    ValueError
        If the Content-Type header is missing or not set to 'application/json'.
        If the body cannot be decoded as valid JSON.
    """
    # Retrieve headers and body
    headers = http_request.get("headers", {})
    body = http_request.get("body")

    # Validate Content-Type header
    content_type = headers.get("Content-Type") or headers.get("content-type")
    if not content_type:
        raise ValueError("Missing 'Content-Type' header.")
    # Normalize and compare
    if content_type.lower().split(";")[0].strip() != "application/json":
        raise ValueError(
            f"Unsupported Content-Type '{content_type}'. Expected 'application/json'."
        )

    # Ensure body is a string or bytes
    if isinstance(body, bytes):
        try:
            body = body.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise ValueError("Body is not valid UTF-8.") from exc
    elif not isinstance(body, str):
        raise ValueError("Body must be a string or bytes containing JSON.")

    # Parse JSON
    try:
        parsed = json.loads(body)
    except json.JSONDecodeError as exc:
        raise ValueError(f"Malformed JSON: {exc.msg}") from exc

    # Ensure the parsed object is a dictionary
    if not isinstance(parsed, dict):
        raise ValueError("JSON body must represent an object (dictionary).")

    return parsed