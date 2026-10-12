import re

# RFC 7230 token characters: !#$%&'*+-.^_`|~ and digits/letters
TOKEN_RE = re.compile(r"^[!#$%&'*+\-.^_`|~0-9a-zA-Z]+$")

def include_custom_header(custom_value: str) -> str:
    """
    Return a full HTTP header string with the custom value safely sanitized.

    Parameters
    ----------
    custom_value : str
        User-provided header field value. Must consist only of valid token characters.

    Returns
    -------
    str
        A header string of the form 'X-Custom-Header: <sanitized_value>'.

    Raises
    ------
    ValueError
        If the input contains characters not allowed in an HTTP token.
    """
    if not isinstance(custom_value, str):
        raise ValueError("Header value must be a string")

    # Ensure the value contains only allowed token characters
    if not TOKEN_RE.fullmatch(custom_value):
        raise ValueError(
            "Header value contains disallowed characters. "
            "Only token characters are permitted: !#$%&'*+-.^_`|~ and alphanumerics."
        )

    # Construct the header
    return f"X-Custom-Header: {custom_value}"