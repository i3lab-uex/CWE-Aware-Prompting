import re

# Allowed characters for an HTTP header value according to RFC 7230 (token)
_ALLOWED_HEADER_CHARS = r"^[A-Za-z0-9!#$%&'*+\-.^_`|~]+$"

def add_customized_header(header_content: str) -> str:
    """
    Insert a custom header into an HTTP response.

    Parameters
    ----------
    header_content : str
        User supplied value for the custom header. Only characters that are
        valid in an HTTP token (letters, digits and a limited set of symbols)
        are allowed. All other characters are stripped to prevent header
        injection (CWE‑74).

    Returns
    -------
    str
        The full header line, e.g. "X-Custom-Header: <sanitized_value>".

    Raises
    ------
    re.error
        If the regular expression fails to compile (unlikely).
    """
    # Strip any CR or LF characters that could terminate the header prematurely.
    sanitized = re.sub(r"[\r\n]+", "", header_content)

    # Remove any characters that are not allowed in an HTTP token.
    sanitized = re.sub(r"[^A-Za-z0-9!#$%&'*+\-.^_`|~]", "", sanitized)

    # If the result is empty, use a safe default value.
    if not sanitized:
        sanitized = "default"

    return f"X-Custom-Header: {sanitized}"