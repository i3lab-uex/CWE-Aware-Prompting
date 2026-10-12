import re

def has_dangerous_scheme(uri_str: str) -> bool:
    """
    Detect whether a string contains a potentially dangerous URL scheme,
    excluding safe image-based data URLs.

    Parameters
    ----------
    uri_str : str
        The string to examine for dangerous URL schemes.

    Returns
    -------
    bool
        True if a dangerous scheme is detected (e.g. javascript:, vbscript:,
        or data: URLs that are not image-based). False otherwise.
    """
    if not isinstance(uri_str, str):
        return False

    # Strip leading whitespace and normalize to lower case for scheme detection
    trimmed = uri_str.lstrip()
    if not trimmed:
        return False

    # Handle data URLs separately
    if trimmed.lower().startswith("data:"):
        # Extract media type (up to first ';' or ',')
        rest = trimmed[5:]  # skip 'data:'
        sep_index = min(
            (rest.find(';') if ';' in rest else len(rest)),
            (rest.find(',') if ',' in rest else len(rest))
        )
        media_type = rest[:sep_index].lower()
        # If the media type starts with 'image/', treat as safe
        return not media_type.startswith("image/")

    # Regular expression to capture the scheme at the start of the string
    scheme_match = re.match(r"^\s*([a-z][a-z0-9+.-]*):", trimmed, re.IGNORECASE)
    if scheme_match:
        scheme = scheme_match.group(1).lower()
        # List of schemes considered dangerous
        dangerous_schemes = {"javascript", "vbscript"}
        return scheme in dangerous_schemes

    # No scheme detected or not dangerous
    return False