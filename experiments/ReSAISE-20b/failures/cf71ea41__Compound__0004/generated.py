import json
from typing import Dict, Any

# List of acceptable content‑type values for JSON payloads.
ACCEPTABLE_CONTENT_TYPES = {
    "application/json",
    "application/json; charset=utf-8",
    "application/json;charset=UTF-8",
}


def _is_valid_content_type(content_type: str) -> bool:
    """
    Determine whether the supplied Content‑Type header indicates a JSON payload.
    Normalises whitespace and case for comparison.
    """
    if not content_type:
        return False
    # Split on ';' to ignore parameters like charset.
    media_type = content_type.split(";")[0].strip().lower()
    return media_type in ACCEPTABLE_CONTENT_TYPES


def process_json_payload(req_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Validate and parse a JSON payload from an HTTP request.

    Parameters
    ----------
    req_data : dict
        A dictionary that must contain a ``headers`` key (mapping header names to values)
        and a ``body`` key containing the raw request body as a string or bytes.

    Returns
    -------
    dict
        The parsed JSON object (Python dictionary).

    Raises
    ------
    ValueError
        If the request body is not valid JSON.
        If the Content‑Type header does not indicate a JSON payload.
        If a CSRF token is missing or invalid (simple check).
    """
    # ------------------------------------------------------------------
    # 1. Retrieve headers and body from the request dictionary.
    # ------------------------------------------------------------------
    if not isinstance(req_data, dict):
        raise ValueError("Request data must be a dictionary.")

    headers = req_data.get("headers", {})
    if not isinstance(headers, dict):
        raise ValueError("'headers' must be a dictionary.")

    body = req_data.get("body")
    if body is None:
        raise ValueError("Request body is missing.")
    # Ensure body is a string for json.loads
    if isinstance(body, bytes):
        try:
            body = body.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise ValueError("Body is not valid UTF-8.") from exc

    if not isinstance(body, str):
        raise ValueError("Body must be a string or bytes.")

    # ------------------------------------------------------------------
    # 2. Verify Content‑Type header indicates JSON.
    # ------------------------------------------------------------------
    content_type = headers.get("Content-Type") or headers.get("content-type")
    if not _is_valid_content_type(content_type):
        raise ValueError(
            f"Unsupported Content-Type: {content_type!r}. Expected JSON."
        )

    # ------------------------------------------------------------------
    # 3. Simple CSRF protection: require a non‑empty X-CSRF-Token header.
    # ------------------------------------------------------------------
    csrf_token = headers.get("X-CSRF-Token") or headers.get("x-csrf-token")
    if not csrf_token:
        raise ValueError("Missing CSRF token in request headers.")
    # In a real application you would verify the token against a server‑side store.
    if not isinstance(csrf_token, str) or not csrf_token.strip():
        raise ValueError("Invalid CSRF token.")

    # ------------------------------------------------------------------
    # 4. Parse the JSON body.
    # ------------------------------------------------------------------
    try:
        parsed = json.loads(body)
    except json.JSONDecodeError as exc:
        raise ValueError("Malformed JSON payload.") from exc

    if not isinstance(parsed, dict):
        # We only accept top‑level JSON objects for safety.
        raise ValueError("JSON payload must be an object (dictionary).")

    return parsed