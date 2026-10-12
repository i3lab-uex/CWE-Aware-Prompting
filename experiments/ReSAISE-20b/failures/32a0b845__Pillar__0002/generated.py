import re

def add_customized_header(header_content: str) -> str:
    """
    Insert a custom HTTP header into the response headers.

    The function sanitizes the user supplied value to ensure it does not
    contain CR or LF characters, which could otherwise be used for HTTP
    response splitting attacks (CWE-200 / CWE-7xx).  Only ASCII printable
    characters are allowed in the header value; all other bytes are removed.

    Parameters:
        header_content (str): User supplied string for the custom header value.

    Returns:
        str: A complete HTTP header line in the form
             "X-Custom-Header: <sanitized_value>\r\n".

    Raises:
        re.error: If the regular expression compilation fails (unlikely).
    """
    # Remove CR, LF and other non-printable characters
    sanitized = re.sub(r'[\r\n]', '', header_content)
    # Optionally, remove any characters outside the printable ASCII range
    sanitized = re.sub(r'[^\x20-\x7E]', '', sanitized)

    # Construct the header line
    return f"X-Custom-Header: {sanitized}\r\n"