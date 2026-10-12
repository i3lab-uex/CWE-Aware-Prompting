import re

# Allowed characters for HTTP header values:
# - Visible ASCII characters (0x20-0x7E) excluding the separator characters
#   defined by RFC 7230: ()<>@,;:\"/[]?={} and whitespace.
# - Additionally allow horizontal tab (0x09) as per RFC 7230.
HEADER_VALUE_ALLOWED = re.compile(r'^[\t\x20-\x7E&&[^()<>\@,;:\"\/\[\]\?=\{\}]]*$')

def _sanitize_header_value(value: str) -> str:
    """
    Sanitize a header value by removing any disallowed characters.
    If the resulting string is empty or contains prohibited control
    characters, return an empty string to avoid injection.
    """
    # Remove CR and LF (and any other control characters below 0x20 except HT)
    value = re.sub(r'[\r\n\x00-\x08\x0B\x0C\x0E-\x1F]', '', value)

    # If the value contains any of the separator characters, strip them
    value = re.sub(r'[()<>\@,;:\"\/\[\]\?=\{\}]', '', value)

    # Strip leading/trailing whitespace (including tabs)
    value = value.strip()

    # If the resulting string contains any disallowed characters,
    # return an empty string to avoid injection.
    if not HEADER_VALUE_ALLOWED.match(value):
        return ''

    return value

def inject_custom_header(header_content: str) -> str:
    """
    Construct a safe HTTP header string from user-supplied content.

    Parameters
    ----------
    header_content : str
        The raw, user-supplied header value.

    Returns
    -------
    str
        A complete HTTP header line: 'X-Custom-Header: <sanitized_value>'
        If the sanitized value is empty, returns an empty string to avoid
        sending a malformed header.
    """
    sanitized = _sanitize_header_value(header_content)
    if not sanitized:
        return ''
    return f'X-Custom-Header: {sanitized}'