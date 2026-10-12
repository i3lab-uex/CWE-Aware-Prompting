import json
from typing import Any, Dict

# Define a set of acceptable content‑type values for JSON payloads.
_JSON_CONTENT_TYPES = {
    "application/json",
    "application/json; charset=utf-8",
    "application/json;charset=UTF-8",
}

def _is_json_content_type(content_type: str) -> bool:
    """
    Check whether the provided content‑type header indicates a JSON payload.
    The check is case‑insensitive and ignores any whitespace around the
    comma‑separated parameters.
    """
    if not content_type:
        return False

    # Split on commas to support multiple MIME types in a single header.
    parts = [p.strip().lower() for p in content_type.split(",")]
    return any(part.startswith("application/json") for part in parts)


def validate_and_parse_json(incoming_req: Dict[str, Any]) -> Dict:
    """
    Validate that the incoming HTTP request contains a JSON body and
    return the parsed dictionary.

    Parameters
    ----------
    incoming_req : dict
        Dictionary containing at least two keys:
            - "headers": a mapping of header names to values.
            - "body"   : the raw request body, which can be a string,
                         bytes or an already parsed dictionary.

    Returns
    -------
    dict
        The JSON payload as a Python dictionary.

    Raises
    ------
    ValueError
        If the content‑type header does not indicate a JSON payload.
        Or if the body cannot be parsed as valid JSON.
    """
    headers = incoming_req.get("headers", {})
    body: Any = incoming_req.get("body")

    # 1. Validate content‑type header
    content_type = headers.get("Content-Type") or headers.get("content-type")
    if not _is_json_content_type(content_type):
        raise ValueError(
            "Unsupported content type. Expected application/json but got "
            f"'{content_type}'."
        )

    # 2. Handle already parsed payloads
    if isinstance(body, dict):
        return body

    # 3. Convert bytes to string if necessary
    if isinstance(body, (bytes, bytearray)):
        try:
            body = body.decode("utf-8")
        except Exception as exc:  # pragma: no cover
            raise ValueError("Failed to decode request body as UTF-8.") from exc

    # 4. Ensure the body is a string before parsing
    if not isinstance(body, str):
        raise ValueError(f"Request body must be a string or dict; got {type(body)}.")

    # 5. Parse JSON
    try:
        parsed = json.loads(body)
    except json.JSONDecodeError as exc:
        raise ValueError(f"Malformed JSON payload: {exc.msg}") from exc

    # 6. Ensure the parsed result is a dictionary
    if not isinstance(parsed, dict):
        raise ValueError(
            f"JSON payload must be an object (dict), got {type(parsed).__name__}."
        )

    return parsed