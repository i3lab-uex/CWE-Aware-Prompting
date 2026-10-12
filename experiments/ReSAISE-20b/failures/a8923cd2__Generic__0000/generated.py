import re

def include_custom_header(custom_value: str) -> str:
    """
    Insert a custom header into an HTTP response, sanitizing the user-provided
    value to ensure it contains only printable ASCII characters (32–126).

    Parameters:
        custom_value (str): The user-supplied header value.

    Returns:
        str: A complete HTTP header line with the sanitized custom value,
             e.g. "X-Custom-Header: <sanitized_value>\r\n".

    Notes:
        - The function removes any character outside the printable ASCII range
          to prevent header injection or malformed responses.
        - If `custom_value` is empty after sanitization, an empty string will be
          used as the header value.
    """
    # Define a regex pattern that matches any character NOT in the printable
    # ASCII range (space to tilde). These characters are removed.
    sanitized = re.sub(r'[^ -~]', '', custom_value)

    # Construct the header line. CRLF is used to terminate HTTP headers.
    return f"X-Custom-Header: {sanitized}\r\n"