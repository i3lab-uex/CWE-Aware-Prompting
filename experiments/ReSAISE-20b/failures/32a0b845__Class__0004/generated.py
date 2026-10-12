import re

def add_customized_header(header_content: str) -> str:
    """
    Insert a custom header into the response headers, ensuring that
    the supplied value is safe for HTTP usage.

    The function sanitizes the input by:
      * Removing any CR or LF characters to prevent header injection.
      * Allowing only printable ASCII characters (0x20-0x7E).
      * Trimming leading/trailing whitespace.

    Parameters
    ----------
    header_content : str
        User supplied value for the custom header.

    Returns
    -------
    str
        The full HTTP header string with a safe value.
    """
    # Remove CR and LF characters
    sanitized = re.sub(r'[\r\n]', '', header_content)

    # Keep only printable ASCII characters (0x20-0x7E)
    sanitized = re.sub(r'[^\x20-\x7E]', '', sanitized)

    # Trim whitespace
    sanitized = sanitized.strip()

    # Construct the header line (e.g., "X-Custom-Header: value")
    return f"X-Custom-Header: {sanitized}"