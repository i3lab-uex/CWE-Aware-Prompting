import re

def check_javascript_scheme(url_str: str) -> bool:
    """
    Detect if the supplied string starts with a potentially dangerous URL scheme
    such as 'javascript:' or 'vbscript:'. Image-based data URLs are explicitly
    ignored, so a string like 'data:image/png;base64,...' is considered safe.

    Parameters
    ----------
    url_str : str
        The string to inspect for dangerous schemes.

    Returns
    -------
    bool
        True if a dangerous scheme is detected; False otherwise.
    """
    # Compile a regex that matches javascript: or vbscript: at the beginning of
    # the string, ignoring leading whitespace and being case‑insensitive.
    # The pattern deliberately does not match data:image URLs.
    _dangerous_scheme_re = re.compile(
        r'^\s*(?:javascript|vbscript)\b',
        flags=re.IGNORECASE | re.ASCII
    )

    # Return True if the pattern matches; otherwise False.
    return bool(_dangerous_scheme_re.search(url_str))