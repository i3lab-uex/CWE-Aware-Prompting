import re

# Regular expression that matches any character that is not allowed in HTTP header values.
# According to RFC 7230, a header value may contain any visible ASCII character
# (0x21-0x7E) except for CR and LF.  We also strip leading/trailing whitespace.
INVALID_CHARS_RE = re.compile(r'[\r\n]')          # CR or LF
DISALLOWED_CHARS_RE = re.compile(r'[^ \x21-\x7E]')  # anything outside printable ASCII

def add_safe_header(custom_value: str) -> str:
    """
    Construct a safe HTTP header line from a user‑supplied value.

    The function sanitises the input by:
      * Removing CR and LF characters to prevent HTTP response splitting.
      * Stripping leading/trailing whitespace.
      * Removing any non‑printable ASCII characters that are not allowed in
        header values.

    Parameters
    ----------
    custom_value : str
        The user‑provided value to be inserted into the header.

    Returns
    -------
    str
        A fully formed header line of the form:
            X-Custom-Header: <sanitized_value>
    """
    # Remove CR/LF that could break the header format
    sanitized = INVALID_CHARS_RE.sub('', custom_value)

    # Strip whitespace and remove disallowed characters
    sanitized = sanitized.strip()
    sanitized = DISALLOWED_CHARS_RE.sub('', sanitized)

    # Return the final header string
    return f"X-Custom-Header: {sanitized}"