import re

def include_custom_header(custom_value: str) -> str:
    """
    Insert a custom header into an HTTP response.

    Parameters
    ----------
    custom_value : str
        The user-supplied header value.  It must be a valid HTTP header field
        value: printable ASCII characters, no control or CRLF characters.

    Returns
    -------
    str
        The complete header line: "X-Custom-Header: <sanitized_value>".

    Notes
    -----
    * The function sanitizes the input by stripping any characters that are not
      allowed in an HTTP header value.
    * It protects against CRLF injection and other header injection attacks
      by allowing only a safe subset of characters.
    """
    # Define a pattern that matches allowed header value characters:
    #  - Printable ASCII from space (32) to tilde (126)
    #  - Exclude CR (13), LF (10), and colon (58) to avoid header breaks.
    # The pattern matches any disallowed character for removal.
    disallowed_pattern = re.compile(r'[^\x20-\x7E]|[\r\n:]')

    # Remove disallowed characters
    sanitized = disallowed_pattern.sub('', custom_value)

    return f"X-Custom-Header: {sanitized}"