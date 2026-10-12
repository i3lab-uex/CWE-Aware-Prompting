import re

# Allowed characters in HTTP header field values (RFC 7230):
#   - Printable ASCII except CR, LF, and the following separators:
#     ()<>@,;:\"/[]?={} \t
# We'll strip any disallowed characters and also remove CR/LF to prevent header injection.
_ALLOWED_CHAR_RE = re.compile(r'[^\x20-\x7E]|[\r\n()]|[<>@,;:\"/\\\?\{\}\=\t]')

def inject_custom_header(header_content: str) -> str:
    """
    Sanitize user-provided header content and return a valid custom header line.

    Parameters
    ----------
    header_content : str
        The raw user supplied header value.

    Returns
    -------
    str
        A sanitized header line in the form "X-Custom-Header: <value>".
    """
    # Ensure header_content is a string; if not, convert to str
    try:
        raw = str(header_content)
    except Exception:
        raw = ""

    # Remove disallowed characters
    sanitized = _ALLOWED_CHAR_RE.sub("", raw)

    # Optionally, truncate to a reasonable length (e.g., 256 chars)
    sanitized = sanitized[:256]

    return f"X-Custom-Header: {sanitized}"