import re

def check_javascript_scheme(url_str: str) -> bool:
    """
    Detect whether a string contains a potentially dangerous URL scheme
    (e.g., javascript:, vbscript:) while allowing safe image data URLs.

    Parameters
    ----------
    url_str : str
        The URL string to inspect.

    Returns
    -------
    bool
        True if a dangerous scheme is found (excluding safe image data URLs),
        False otherwise.
    """
    # Regular expression to capture the scheme at the beginning of the string
    # (ignoring leading whitespace).  A scheme is defined as a sequence of
    # letters, digits, '+', '-', or '.' that ends with a colon.
    scheme_re = re.compile(r'^\s*([a-zA-Z][-\w+.]*)\s*:', re.IGNORECASE)

    match = scheme_re.match(url_str)
    if not match:
        return False

    scheme = match.group(1).lower()

    # List of schemes that are considered dangerous
    dangerous_schemes = {"javascript", "vbscript", "data"}

    # If the scheme is not in the dangerous list, it's safe
    if scheme not in dangerous_schemes:
        return False

    # Handle the special case of data URLs.  Allow only image/* types.
    if scheme == "data":
        # Extract the MIME type part before the first comma
        try:
            mime_type = url_str.split(',', 1)[0].split(';', 1)[0]
        except Exception:
            return True  # malformed data URL – treat as dangerous

        if mime_type.lower().startswith("image/"):
            return False  # safe image data URL
        else:
            return True   # non‑image data URLs are dangerous

    # For all other schemes in the dangerous list, flag as dangerous
    return True