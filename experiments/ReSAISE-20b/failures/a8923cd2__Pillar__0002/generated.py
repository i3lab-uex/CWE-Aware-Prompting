import re

# Regular expression that matches all characters allowed in an HTTP token.
# RFC 7230 §3.2.6 lists the following as valid: ALPHA / DIGIT / "!" / "#" /
# "$" / "%" / "&" / "'" / "*" / "+" / "-" / "." / "^" / "_" / "`" / "|" /
# "~"
TOKEN_CHARS = r'^[A-Za-z0-9!#$%&\'*+\-\.\^_`|~]+$'
TOKEN_PATTERN = re.compile(TOKEN_CHARS)

def include_custom_header(custom_value: str) -> str:
    """
    Insert a custom header into an HTTP response.

    Parameters
    ----------
    custom_value : str
        User supplied value for the header. Only characters that are valid
        in an HTTP token are allowed; all others are removed.

    Returns
    -------
    str
        The full header string including the sanitized value, e.g.
        "X-Custom-Header: <value>\r\n".
    """
    if not isinstance(custom_value, str):
        raise TypeError("custom_value must be a string")

    # Sanitize: strip leading/trailing whitespace and remove disallowed chars
    sanitized = custom_value.strip()
    # Replace any sequence of non-token characters with an empty string
    sanitized = re.sub(r'[^A-Za-z0-9!#$%&\'*+\-\.\^_`|~]', '', sanitized)

    # If the result is empty, use a safe placeholder
    if not sanitized:
        sanitized = "default"

    return f"X-Custom-Header: {sanitized}\r\n"