import re

def add_customized_header(header_content: str) -> str:
    """
    Insert a custom header into an HTTP response.

    The function sanitizes the user-provided `header_content` by:
        * Removing any characters that are not printable ASCII (0x20-0x7E).
        * Rejecting any CR or LF characters to prevent header injection.

    Parameters
    ----------
    header_content : str
        The user-supplied value for the custom header.

    Returns
    -------
    str
        A single HTTP header line in the form:
            "X-Custom-Header: <sanitized_value>\r\n"

    Raises
    ------
    ValueError
        If the input contains CR or LF characters after sanitization.
    """
    # First, strip any carriage return / line feed that could lead to injection
    if "\r" in header_content or "\n" in header_content:
        raise ValueError("Header content must not contain CR or LF characters.")

    # Remove non-printable ASCII characters
    sanitized = re.sub(r"[^\x20-\x7E]", "", header_content)

    # Return the complete header line
    return f"X-Custom-Header: {sanitized}\r\n"