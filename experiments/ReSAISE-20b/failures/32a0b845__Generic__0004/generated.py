import re

def add_customized_header(header_content: str) -> str:
    """
    Insert a custom header into an HTTP response string.

    Parameters
    ----------
    header_content : str
        The user-provided value for the custom header.

    Returns
    -------
    str
        A complete HTTP header line with the sanitized value, e.g.
        "X-Custom-Header: <sanitized_value>".

    Notes
    -----
    - Only ASCII printable characters (0x20–0x7E) are allowed.
      Any other character is stripped to avoid header injection
      or formatting issues.
    - The function does not raise explicit exceptions; any regex errors
      will propagate as `re.error`.
    """
    # Remove non‑ASCII printable characters to avoid header injection.
    sanitized = re.sub(r'[^\x20-\x7E]', '', header_content)

    # Ensure that the header value does not contain CR or LF,
    # which could break HTTP formatting.
    sanitized = sanitized.replace('\r', '').replace('\n', '')

    return f"X-Custom-Header: {sanitized}"