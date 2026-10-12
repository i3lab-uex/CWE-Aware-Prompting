import re

def add_customized_header(header_content: str) -> str:
    """
    Return a full HTTP header string with the user supplied value inserted
    as a custom header named "X-Custom-Header". The value is sanitized to
    prevent HTTP response splitting and other injection attacks.

    Parameters
    ----------
    header_content : str
        The user supplied string to be used as the header value.

    Returns
    -------
    str
        The complete header line including CRLF termination.

    Raises
    ------
    re.error
        If the regular expression fails to compile (unlikely in this context).
    """
    # Remove CR, LF and other control characters that could terminate the header
    # or inject additional headers/lines.
    sanitized = re.sub(r'[\r\n]+', '', header_content)

    # Additionally strip any non-printable characters that might be
    # interpreted specially by downstream HTTP processing.
    sanitized = re.sub(r'[\x00-\x1F\x7F]', '', sanitized)

    # Ensure the header value does not contain leading or trailing whitespace
    sanitized = sanitized.strip()

    return f"X-Custom-Header: {sanitized}\r\n"