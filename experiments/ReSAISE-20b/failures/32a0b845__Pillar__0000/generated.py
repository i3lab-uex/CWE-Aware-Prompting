import re

# Regular expression to match any character that is NOT a printable ASCII character (except space)
# Printable ASCII range: 0x20 (space) to 0x7E (~). We exclude CR, LF, and other control chars.
_SANITIZE_PATTERN = re.compile(r'[^ -~]')

def add_customized_header(header_content: str) -> str:
    """
    Insert a custom header into the HTTP response headers.

    The function sanitizes `header_content` by removing any characters that are
    not printable ASCII (excluding space). This mitigates header injection attacks
    such as CRLF injection.

    Parameters:
        header_content (str): User supplied value for the custom header.

    Returns:
        str: The complete header string in the form
             "X-Custom-Header: <sanitized_value>\r\n".

    Raises:
        re.error: If the regular expression fails to compile or match (unlikely).
    """
    # Sanitize the input: remove any non-printable ASCII characters
    sanitized = _SANITIZE_PATTERN.sub('', header_content)

    # Construct the full header string
    return f"X-Custom-Header: {sanitized}\r\n"