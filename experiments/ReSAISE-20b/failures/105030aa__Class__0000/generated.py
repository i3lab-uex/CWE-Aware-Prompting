import re

def add_custom_header(header_value: str) -> str:
    """
    Return a safe HTTP header line containing the user‑supplied value.

    The function sanitizes the input by removing any carriage return or line feed
    characters, which could otherwise allow HTTP response splitting or other
    injection attacks (CWE‑74).  Only printable ASCII characters are allowed.
    Non‑printable or control characters are stripped.

    Parameters
    ----------
    header_value : str
        The user supplied value for the custom header.

    Returns
    -------
    str
        A complete HTTP header line, e.g. "Custom-Header: value\r\n".

    Raises
    ------
    re.error
        If an invalid regex pattern is used (unlikely with the hard‑coded patterns).
    """
    # Remove CR, LF and any other control characters (ASCII 0x00‑0x1F) from the value
    sanitized = re.sub(r'[\r\n\x00-\x1F]', '', header_value)

    # Optionally, collapse multiple spaces into a single space to avoid weird formatting
    sanitized = re.sub(r'\s+', ' ', sanitized).strip()

    # Construct the header line
    return f"Custom-Header: {sanitized}\r\n"