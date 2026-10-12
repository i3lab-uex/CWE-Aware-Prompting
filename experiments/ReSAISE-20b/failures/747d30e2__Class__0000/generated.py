import re

def is_javascript_scheme(s: str) -> bool:
    """
    Detects whether a string contains a potentially malicious URL scheme
    (javascript, jscript, vbscript) while ignoring image data URLs.

    Parameters
    ----------
    s : str
        The string to be checked for malicious URL schemes.

    Returns
    -------
    bool
        True if a malicious scheme is found, False otherwise.
    """
    if not isinstance(s, str):
        return False

    # Strip leading whitespace for the check
    trimmed = s.lstrip()

    # Exclude image data URLs (e.g., data:image/png;base64,...)
    if trimmed.lower().startswith("data:"):
        # If the data URL is an image, it's considered safe
        if re.match(r"data\s*:\s*image\/", trimmed, flags=re.IGNORECASE):
            return False

    # Pattern for malicious schemes at the beginning of the string
    malicious_pattern = re.compile(r"^(javascript|jscript|vbscript)\b", flags=re.IGNORECASE)

    return bool(malicious_pattern.match(trimmed))