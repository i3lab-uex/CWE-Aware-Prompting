import re

# Regular expression that matches any character NOT allowed in HTTP header values.
# Allowed characters: printable ASCII except CR (0x0D) and LF (0x0A).
# We also disallow non‑printable control characters.
_disallowed_header_chars = re.compile(r'[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]|[\r\n]')

def inject_custom_header(header_content: str) -> str:
    """
    Construct a safe custom HTTP header line from user‑supplied content.

    The function sanitises the input by removing any control characters,
    line breaks, or other non‑printable ASCII that could be used to inject
    additional headers or break the HTTP protocol.  The resulting header line
    is safe to include in an HTTP response.

    Parameters
    ----------
    header_content : str
        The raw user‑supplied custom header value.

    Returns
    -------
    str
        A single line string in the form "X-Custom-Header: <sanitized value>".

    Notes
    -----
    - The header name is fixed to "X-Custom-Header" to avoid user control
      over the header field name, which could be abused for other attacks.
    - If the input is an empty string or becomes empty after sanitisation,
      a default placeholder value ("") is used to avoid creating an
      invalid header line.
    """
    if not isinstance(header_content, str):
        # Coerce non‑string input to string; this is defensive but keeps the
        # function simple for callers that might pass other types.
        header_content = str(header_content)

    # Remove disallowed characters
    sanitized_value = _disallowed_header_chars.sub('', header_content)

    # Ensure the value is not empty; if it is, use an empty string placeholder.
    if sanitized_value == '':
        sanitized_value = ''

    # Construct the final header line
    return f"X-Custom-Header: {sanitized_value}"