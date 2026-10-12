import re

def add_customized_header(header_content: str) -> str:
    """
    Insert a custom header into the response headers.

    The function sanitizes the user-supplied `header_content` by removing any
    characters that are not permitted in a standard HTTP header field value.
    Only ASCII letters, digits, space and the characters '-', '.', '_' are
    allowed. Any other character is stripped out.

    Parameters
    ----------
    header_content : str
        The user-provided value for the custom header.

    Returns
    -------
    str
        A string containing a single HTTP header line, e.g.
        "X-Custom: sanitized_value".

    Notes
    -----
    - The function does not raise explicit exceptions; if the regular
      expression fails, a ``re.error`` will propagate.
    - This implementation is intentionally simple and aimed at preventing
      injection of non‑printable or control characters into the header.
    """
    # Allow only printable ASCII letters, digits and a few safe punctuation
    sanitized = re.sub(r'[^A-Za-z0-9 \-\.\_]', '', header_content)

    # Ensure the sanitized string is not empty; if it becomes empty,
    # default to a placeholder value.
    if not sanitized:
        sanitized = "default"

    return f"X-Custom: {sanitized}"