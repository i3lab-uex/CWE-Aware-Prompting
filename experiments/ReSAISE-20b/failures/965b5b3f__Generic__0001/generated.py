import json
from typing import Dict, Any

def process_json_request(req_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Parse and validate the body of an incoming JSON request.

    Parameters
    ----------
    req_data : dict
        A dictionary containing at least the keys 'headers' and 'body'.
        ``req_data['headers']`` should be a mapping of header names to values.
        ``req_data['body']`` may be a bytes or str instance containing the raw
        request payload.

    Returns
    -------
    dict
        The decoded JSON object.

    Raises
    ------
    ValueError
        If the Content-Type header is missing or does not indicate JSON.
        If the body cannot be decoded as valid JSON.
    """
    headers = req_data.get("headers", {})
    content_type = headers.get("Content-Type") or headers.get("content-type")

    if not content_type:
        raise ValueError("Missing Content-Type header.")

    # Accept only application/json or its variants (e.g., with charset)
    if not content_type.lower().startswith("application/json"):
        raise ValueError(
            f"Unsupported Content-Type '{content_type}'. Expected 'application/json'."
        )

    body = req_data.get("body")
    if body is None:
        raise ValueError("Missing request body.")

    # Convert bytes to str if necessary
    if isinstance(body, (bytes, bytearray)):
        try:
            body_text = body.decode("utf-8")
        except Exception as exc:  # pragma: no cover
            raise ValueError("Body is not valid UTF-8.") from exc
    elif isinstance(body, str):
        body_text = body
    else:
        raise ValueError(f"Unsupported body type: {type(body).__name__}")

    try:
        parsed = json.loads(body_text)
    except json.JSONDecodeError as exc:
        raise ValueError(f"Invalid JSON payload: {exc.msg}") from exc

    if not isinstance(parsed, dict):
        raise ValueError("JSON payload must be an object (dictionary).")

    return parsed