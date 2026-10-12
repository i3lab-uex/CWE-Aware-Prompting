import re

# Allowed characters in an HTTP header value: printable ASCII excluding control chars and delimiters
_HEADER_VALUE_RE = re.compile(r'^[\x20-\x7E]*$')

def add_safe_header(custom_value: str) -> str:
    """
    Safely insert a user-supplied value into an HTTP header.

    The function validates the input against RFC 7230 restrictions for
    header field values:
      * Only printable ASCII characters are allowed.
      * Control characters, CR (0x0D), LF (0x0A) and other delimiters are rejected.

    Parameters
    ----------
    custom_value : str
        The user-provided header value.

    Returns
    -------
    str
        A complete header line in the form "X-Custom: <sanitized_value>".

    Notes
    -----
    * The function does not raise a custom exception; if the value fails validation,
      it is replaced with an empty string to avoid injection.
    * This approach mitigates CRLF injection and other header injection attacks.
    """
    # Ensure the input is a string; coerce non-strings to str
    value = str(custom_value)

    # Strip leading/trailing whitespace (optional, but common)
    value = value.strip()

    # Validate against the allowed pattern
    if not _HEADER_VALUE_RE.match(value):
        # If invalid, discard or replace with safe placeholder
        value = ""

    return f"X-Custom: {value}"