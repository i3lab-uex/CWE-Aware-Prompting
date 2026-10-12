import re

def verify_javascript_protocol(url_input: str) -> bool:
    """
    Detect potentially dangerous URL schemes such as `javascript:` or `vbscript:`
    while allowing safe image data URLs (e.g., `data:image/png;base64,...`).

    Parameters
    ----------
    url_input : str
        The string to examine for possible dangerous URL schemes.

    Returns
    -------
    bool
        True if a potentially harmful scheme is detected, False otherwise.
    """
    if not isinstance(url_input, str):
        # Non‑string input is treated as safe
        return False

    # Strip leading/trailing whitespace and lowercase for case‑insensitive matching.
    trimmed = url_input.strip().lower()

    # Quick check: if it doesn't contain a colon, it's not a scheme.
    if ':' not in trimmed:
        return False

    # Extract the scheme part (before the first colon).
    scheme = trimmed.split(':', 1)[0]

    # Dangerous schemes.
    if scheme in {'javascript', 'vbscript'}:
        return True

    # Handle data URLs: allow only image types.
    if scheme == 'data':
        # A valid image data URL has the form: data:image/<type>;base64,....
        # We check that it contains `image/` and a semicolon after the MIME type.
        if re.search(r'^data:image/\w+;base64,', trimmed):
            return False  # safe
        else:
            # Any other data:URL is considered dangerous.
            return True

    # All other schemes are considered safe for this check.
    return False