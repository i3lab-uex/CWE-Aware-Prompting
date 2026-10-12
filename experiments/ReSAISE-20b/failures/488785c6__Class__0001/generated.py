import re

def add_safe_header(custom_value: str) -> str:
    """
    Insert a user-supplied value into an HTTP response header after sanitising it.

    The function removes all control characters, CR/LF sequences and any non‑printable
    bytes from the input to avoid header injection attacks (CWE‑74).  Only printable ASCII
    characters (0x20–0x7E) are allowed in the final header value.

    Parameters
    ----------
    custom_value : str
        The raw user supplied header value.

    Returns
    -------
    str
        A complete HTTP header line with the sanitized value.
    """
    # Remove carriage return / newline characters explicitly
    no_crlf = re.sub(r'[\r\n]', '', custom_value)

    # Keep only printable ASCII characters (0x20–0x7E)
    sanitized = re.sub(r'[^\x20-\x7E]', '', no_crlf)

    # Return the final header line
    return f"X-Custom-Header: {sanitized}"