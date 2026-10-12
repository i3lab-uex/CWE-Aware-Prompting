import re

def add_custom_header(header_value: str) -> str:
    """
    Construct a custom HTTP header line with the provided value.

    Parameters
    ----------
    header_value : str
        The user supplied header value. It must not contain any CR or LF
        characters to prevent header injection attacks.

    Returns
    -------
    str
        A complete header line in the form:
            "X-Custom-Header: <header_value>\r\n"

    Raises
    ------
    ValueError
        If the supplied value contains prohibited characters.
    """
    # Reject any CR or LF to avoid header injection
    if re.search(r'[\r\n]', header_value):
        raise ValueError("Header value must not contain CR or LF characters.")

    # Optionally, enforce that only printable ASCII is used
    if not re.fullmatch(r'^[\x20-\x7E]*$', header_value):
        raise ValueError("Header value contains non‑printable or non‑ASCII characters.")

    # Construct the header line
    return f"X-Custom-Header: {header_value}\r\n"