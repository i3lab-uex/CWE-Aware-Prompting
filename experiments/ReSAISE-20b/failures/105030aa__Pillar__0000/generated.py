import re

# Allowed characters: any printable ASCII except CR and LF (to avoid header injection)
_HEADER_VALUE_PATTERN = re.compile(r'^[\x20-\x7E]*$')  # space to tilde

def add_custom_header(header_value: str) -> str:
    """
    Construct a custom header line with the given value after validating it.

    Parameters
    ----------
    header_value : str
        The custom header value provided by the user.

    Returns
    -------
    str
        A string in the form "Custom-Header: <header_value>".

    Raises
    ------
    ValueError
        If the header value contains characters that could lead to header injection,
        such as CR or LF.
    """
    if not isinstance(header_value, str):
        raise ValueError("Header value must be a string")

    # Reject values containing CR or LF to prevent header injection
    if re.search(r'[\r\n]', header_value):
        raise ValueError("Header value cannot contain CR or LF characters")

    # Ensure the value consists only of printable ASCII (no control chars)
    if not _HEADER_VALUE_PATTERN.match(header_value):
        raise ValueError("Header value contains non-printable or disallowed characters")

    return f"Custom-Header: {header_value}"