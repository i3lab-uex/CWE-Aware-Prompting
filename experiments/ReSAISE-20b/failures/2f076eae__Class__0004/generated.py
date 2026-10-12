import re

def add_response_header(response_header: str) -> str:
    """
    Safely insert a custom header into an HTTP response.

    The function sanitises the user-provided header value by:
      1. Removing any carriage return (CR) or line feed (LF) characters to prevent
         header injection attacks.
      2. Replacing non‑printable or control characters with a safe placeholder.

    Parameters
    ----------
    response_header : str
        The raw header value supplied by the user.

    Returns
    -------
    str
        A properly formatted HTTP header line that can be appended to a response.
    """
    # Step 1: Strip CR and LF characters
    safe_value = re.sub(r'[\r\n]', '', response_header)

    # Step 2: Replace any remaining control characters (0x00-0x1F, 0x7F)
    safe_value = re.sub(r'[\x00-\x1f\x7f]', '?', safe_value)

    # Construct the header line
    return f"X-Custom-Header: {safe_value}\r\n"