import re

def insert_header_with_sanitization(custom_header_value: str) -> str:
    """
    Sanitize a user-supplied header value and return a complete HTTP header line.

    The function removes all control characters (CR, LF, etc.) and collapses
    whitespace to a single space.  It then constructs a header string in the form
    "X-Custom-Header: <sanitized_value>".

    Parameters
    ----------
    custom_header_value : str
        The raw header value supplied by the user.

    Returns
    -------
    str
        A safe, well‑formed header line ready to be appended to an HTTP response.

    Notes
    -----
    * Control characters that could terminate the header line or inject additional
      headers are stripped out.
    * Tab characters are preserved as they are valid whitespace in HTTP header
      values, but all other non‑printable characters are removed.
    * The function is intentionally permissive with printable ASCII; if stricter
      validation (e.g., allowing only a subset of characters) is required, the
      regular expression can be tightened accordingly.
    """
    # Remove carriage return, line feed and other control characters
    sanitized = re.sub(r'[\r\n\x00-\x08\x0B\x0C\x0E-\x1F]', '', custom_header_value)

    # Collapse any remaining whitespace (spaces, tabs) into a single space
    sanitized = re.sub(r'\s+', ' ', sanitized).strip()

    # Construct the final header line
    return f"X-Custom-Header: {sanitized}"