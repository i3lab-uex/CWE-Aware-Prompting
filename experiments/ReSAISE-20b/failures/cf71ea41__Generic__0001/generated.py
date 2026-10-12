import json
from typing import Dict, Any


def process_json_payload(req_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Validate and parse a JSON payload from an HTTP request.

    Parameters
    ----------
    req_data : dict
        A dictionary that must contain the keys:
            - ``headers`` : a mapping of header names to values
            - ``body``    : the raw request body (bytes or str)

    Returns
    -------
    dict
        The parsed JSON payload.

    Raises
    ------
    ValueError
        If the ``Content-Type`` header is missing or not JSON-compatible,
        or if the body cannot be decoded as valid JSON.
    """
    # ------------------------------------------------------------------
    # 1. Retrieve headers and body
    # ------------------------------------------------------------------
    headers = req_data.get("headers", {})
    if not isinstance(headers, dict):
        raise ValueError("Headers must be a dictionary")

    body = req_data.get("body")
    if body is None:
        raise ValueError("Request body is missing")

    # ------------------------------------------------------------------
    # 2. Validate Content-Type header
    # ------------------------------------------------------------------
    content_type = headers.get("Content-Type") or headers.get("content-type")
    if not content_type:
        raise ValueError("Missing 'Content-Type' header")

    # Accept common JSON MIME types
    json_mime_types = {
        "application/json",
        "application/json; charset=utf-8",
        "application/json;charset=utf-8",
    }
    if not any(ct.lower().startswith(mt) for ct in [content_type] for mt in json_mime_types):
        raise ValueError(
            f"Unsupported Content-Type '{content_type}'. Expected a JSON-compatible type."
        )

    # ------------------------------------------------------------------
    # 3. Decode body (bytes → str) if necessary
    # ------------------------------------------------------------------
    if isinstance(body, bytes):
        try:
            body_str = body.decode("utf-8")
        except Exception as exc:  # pragma: no cover
            raise ValueError("Body bytes could not be decoded as UTF-8") from exc
    elif isinstance(body, str):
        body_str = body
    else:  # pragma: no cover
        raise ValueError("Body must be a string or bytes")

    # ------------------------------------------------------------------
    # 4. Parse JSON
    # ------------------------------------------------------------------
    try:
        payload = json.loads(body_str)
    except json.JSONDecodeError as exc:  # pragma: no cover
        raise ValueError("Malformed JSON payload") from exc

    if not isinstance(payload, dict):
        raise ValueError("JSON payload must be an object (dict)")

    return payload