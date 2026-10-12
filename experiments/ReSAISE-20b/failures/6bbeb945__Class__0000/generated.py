import re

def has_dangerous_scheme(uri_str: str) -> bool:
    """
    Determine whether a given URI string contains a potentially dangerous
    scheme such as `javascript:` or `vbscript:`, while ignoring safe image
    data URLs (e.g., `data:image/...`).

    Parameters
    ----------
    uri_str : str
        The URI string to examine.

    Returns
    -------
    bool
        True if a dangerous scheme is present; False otherwise.
    """
    # Compile a case‑insensitive regex that matches the dangerous schemes
    # at the beginning of the string, allowing optional leading whitespace.
    _dangerous_scheme_re = re.compile(r'^\s*(?:javascript|vbscript):', re.IGNORECASE)

    # If the regex matches, we have a dangerous scheme.
    return bool(_dangerous_scheme_re.match(uri_str))