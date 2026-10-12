import re

def insert_custom_header(custom_header: str) -> str:
    """
    Insert a custom header into an HTTP response.

    Parameters
    ----------
    custom_header : str
        The value of the header to be inserted.  It must not contain CR or LF
        characters, as those would break the HTTP header format.

    Returns
    -------
    str
        A string containing a single complete HTTP header line,
        e.g. "Custom-Header: <value>\r\n".

    Notes
    -----
    The function performs a lightweight validation using a regular expression
    to ensure that the header value does not contain any line‑break characters.
    It deliberately avoids more complex validation to keep the function
    lightweight and portable.  If you need stricter header value checks,
    extend the regular expression or add additional logic.
    """
    # Basic validation: ensure no CR/LF characters are present
    if not re.fullmatch(r"[^\r\n]*", custom_header):
        raise ValueError("Header value contains invalid characters (CR/LF).")

    # Construct the header line
    return f"Custom-Header: {custom_header}\r\n"