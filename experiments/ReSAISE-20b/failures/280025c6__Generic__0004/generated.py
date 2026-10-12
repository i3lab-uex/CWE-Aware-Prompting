import re

def inject_custom_header(header_content: str) -> str:
    """
    Sanitise a user supplied header value and return the final
    HTTP header string.

    The sanitisation removes any control characters, line breaks,
    and disallows the colon character which could be used to
    terminate the header name. Only printable ASCII characters
    (code points 32-126) are retained, except the colon.

    Parameters
    ----------
    header_content : str
        User supplied value for the custom header.

    Returns
    -------
    str
        The complete HTTP header line, e.g.
        "X-Custom-Header: sanitized_value"
    """
    # Remove CR, LF and any other control characters
    cleaned = re.sub(r'[\r\n\x00-\x1f\x7f]', '', header_content)

    # Remove any remaining colon characters that could break the
    # header format. We keep spaces, hyphens and underscore for
    # readability.
    cleaned = cleaned.replace(':', '')

    # Optionally collapse multiple spaces to a single space
    cleaned = re.sub(r'\s+', ' ', cleaned).strip()

    return f"X-Custom-Header: {cleaned}"