import json
from typing import Any, Dict


def parse_json_request(request: Dict[str, Any]) -> Dict[str, Any]:
    """
    Parse and validate a JSON request body.

    Parameters
    ----------
    request : dict
        The request object containing at least a 'body' key. The body may be a
        string, bytes or already-decoded dict.

    Returns
    -------
    dict
        The decoded JSON body as a dictionary.

    Raises
    ------
    ValueError
        If the request does not contain a body, if JSON decoding fails,
        or if the decoded value is not a dictionary.
    """
    # 1. Ensure body key exists
    if "body" not in request:
        raise ValueError("Missing 'body' key in request")

    body = request["body"]

    # 2. If the body is already a dict, return it directly
    if isinstance(body, dict):
        return body

    # 3. If the body is bytes, decode to str
    if isinstance(body, (bytes, bytearray)):
        try:
            body = body.decode("utf-8")
        except Exception as exc:  # pragma: no cover
            raise ValueError(f"Failed to decode body bytes: {exc}") from exc

    # 4. Body should now be a string
    if not isinstance(body, str):
        raise ValueError(f"Unexpected body type: {type(body).__name__}")

    # 5. Parse JSON
    try:
        parsed = json.loads(body)
    except json.JSONDecodeError as exc:
        raise ValueError(f"JSON decoding failed: {exc.msg}") from exc

    # 6. Ensure the parsed JSON is a dictionary
    if not isinstance(parsed, dict):
        raise ValueError(
            f"Parsed JSON is not a dictionary (type={type(parsed).__name__})"
        )

    return parsed