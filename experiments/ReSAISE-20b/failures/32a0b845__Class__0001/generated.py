import re

def add_customized_header(header_content: str) -> str:
    """
    Insert a custom header into an HTTP response string.

    The supplied `header_content` is sanitized to prevent CRLF injection
    (CWE‑74). Any carriage return or line feed characters are removed,
    ensuring the header value cannot break out of its field and inject
    additional headers or control characters.

    Parameters:
        header_content (str): User‑defined value for the custom header.

    Returns:
        str: A single HTTP header line including a CRLF terminator.
    """
    # Remove any carriage return or line feed characters
    sanitized = re.sub(r'[\r\n]', '', header_content)

    # Construct the header line (using a custom name to avoid clashes)
    return f"X-Custom-Header: {sanitized}\r\n"