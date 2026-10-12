import re

def insert_header_with_sanitization(custom_header_value: str) -> str:
    """
    Safely construct an HTTP header string from a user supplied value.

    The function removes any CR/LF characters that could be used to
    inject additional headers (CWE‑74).  It also restricts the value
    to characters that are allowed in HTTP header values (token or
    quoted string).  If the value contains only whitespace, it is
    replaced with an empty string.

    Parameters
    ----------
    custom_header_value : str
        The user supplied header value.

    Returns
    -------
    str
        A well‑formed HTTP header string of the form:
            "X-Custom-Header: <sanitized_value>"
    """
    # Strip leading/trailing whitespace
    value = custom_header_value.strip()

    # Remove CR and LF characters to prevent header injection
    value = re.sub(r'[\r\n]+', '', value)

    # Allow only printable ASCII characters that are not control
    # or separators.  This is a conservative subset of the token
    # and quoted-string allowed by RFC 7230.
    # Control chars: 0x00-0x1F, 0x7F
    # Separators: ()<>@,;:\"/[]?={} \t
    value = re.sub(r'[^ -~]', '', value)          # keep printable ASCII
    value = re.sub(r'[()<>@,;:\\\"/\\[\\]\\?=\\{\\}\\s]', '', value)

    # If after sanitization nothing remains, use a safe default
    if not value:
        value = "empty"

    return f"X-Custom-Header: {value}"