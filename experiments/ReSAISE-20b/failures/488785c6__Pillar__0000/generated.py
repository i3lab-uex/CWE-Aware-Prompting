import re

# Regular expression that matches a safe header value:
#   - Only printable ASCII characters except CR and LF
#   - Allows spaces, hyphens, underscores, dots, and alphanumerics
#   - Rejects any control characters or non‑printable bytes
_SAFE_HEADER_RE = re.compile(r'^[\x20-\x7E]+$')

def add_safe_header(custom_value: str) -> str:
    """
    Return a safe HTTP header string containing the user supplied value.

    The function validates that `custom_value` contains only printable ASCII
    characters (except CR and LF).  It also strips leading/trailing whitespace.
    If the value fails validation, an empty string is returned so that no
    malformed header can be sent.

    Parameters:
        custom_value (str): The user supplied value for the custom header.

    Returns:
        str: A string of the form "X-Custom-Header: <sanitized_value>" or an
        empty string if validation fails.
    """
    # Strip whitespace to avoid accidental CRLF injection via leading/trailing spaces
    value = custom_value.strip()

    # Validate against the safe header regex; reject if any disallowed character
    if not _SAFE_HEADER_RE.match(value):
        # Invalid value – return an empty header to avoid sending a bad one
        return ""

    # Build the final header string
    header = f"X-Custom-Header: {value}"
    return header