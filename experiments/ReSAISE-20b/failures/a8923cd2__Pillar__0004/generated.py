import re

def include_custom_header(custom_value: str) -> str:
    """
    Insert a custom HTTP header into the response headers.

    Parameters
    ----------
    custom_value : str
        User-supplied value for the custom header.

    Returns
    -------
    str
        A string representing the full HTTP header line with a sanitized
        custom value.

    Notes
    -----
    * The function removes any carriage return or line feed characters from the
      input to prevent HTTP response splitting (CWE‑20 & CWE‑707).
    * It also strips any control characters that are not printable to avoid
      malformed headers.
    """
    # Remove CR and LF characters (potential line breaks)
    sanitized = re.sub(r'[\r\n]', '', custom_value)

    # Remove other control characters (ASCII 0x00–0x1F and 0x7F)
    sanitized = re.sub(r'[\x00-\x1F\x7F]', '', sanitized)

    # Ensure the resulting header value is not empty
    if not sanitized:
        raise ValueError("Custom header value must contain at least one printable character.")

    # Construct the full header line (example: "X-Custom-Header: <value>")
    return f"X-Custom-Header: {sanitized}"