import re

def inject_custom_header(header_content: str) -> str:
    """
    Sanitize a user-supplied header value and return a complete HTTP header string.

    Parameters
    ----------
    header_content : str
        The raw user-provided header value.

    Returns
    -------
    str
        A string in the form "X-Custom-Header: <sanitized_value>" ready to be added
        to an HTTP response.

    Notes
    -----
    - Removes any carriage return or line feed characters to prevent header injection.
    - Strips leading/trailing whitespace and removes non-printable ASCII characters
      (i.e., anything outside the range 0x20–0x7E).
    - The function does not raise exceptions; any regex errors will propagate
      normally.
    """
    # Step 1: Remove CR and LF characters to avoid header injection
    sanitized = re.sub(r'[\r\n]+', '', header_content)

    # Step 2: Strip leading/trailing whitespace
    sanitized = sanitized.strip()

    # Step 3: Remove any non-printable ASCII characters (outside 0x20–0x7E)
    sanitized = re.sub(r'[^\x20-\x7E]', '', sanitized)

    # If the resulting header is empty, default to an empty string
    if not sanitized:
        sanitized = ""

    return f"X-Custom-Header: {sanitized}"