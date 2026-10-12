import re

# Regular expression that matches a header value containing only printable ASCII characters
# (space to tilde) and excludes CR (\r), LF (\n) and other control characters.
# The pattern also ensures that the value is non‑empty after stripping whitespace.
HEADER_VALUE_RE = re.compile(r'^[\x20-\x7E]+$')

def inject_custom_header(header_content: str) -> str:
    """
    Return a properly formatted custom HTTP header string with the supplied value
    sanitized to prevent CRLF injection and other malformed inputs.

    Parameters
    ----------
    header_content : str
        The user‑supplied value to be inserted as the custom header.

    Returns
    -------
    str
        The final header string in the form "X-Custom-Header: <sanitized_value>".

    Raises
    ------
    re.error
        If the regular expression fails to compile (unlikely in this context).
    """
    # Strip leading/trailing whitespace to avoid accidental injection.
    value = header_content.strip()

    # Reject empty values outright.
    if not value:
        raise ValueError("Header content cannot be empty.")

    # Ensure the value contains only allowed printable ASCII characters.
    if not HEADER_VALUE_RE.match(value):
        raise ValueError("Header content contains invalid characters.")

    # Construct the final header string.
    return f"X-Custom-Header: {value}"