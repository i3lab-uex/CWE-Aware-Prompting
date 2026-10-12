import re

def verify_javascript_protocol(url_input: str) -> bool:
    """
    Detect potentially dangerous URL schemes such as `javascript:` or `vbscript:`,
    while explicitly allowing image data URLs (e.g., `data:image/...`).

    Parameters
    ----------
    url_input : str
        The URL or string to examine.

    Returns
    -------
    bool
        ``True`` if a dangerous scheme is detected; ``False`` otherwise.
    """
    if not isinstance(url_input, str):
        # Non‑string inputs are considered safe by definition.
        return False

    # Trim leading/trailing whitespace for a stricter match.
    trimmed = url_input.strip()

    # 1. Allow image data URLs – these are explicitly considered safe.
    if re.match(r'^data:image/', trimmed, flags=re.IGNORECASE):
        return False

    # 2. Detect dangerous schemes (case‑insensitive).
    #    We look for a scheme followed by ':' at the start of the string.
    if re.match(r'^\s*(javascript|vbscript):', trimmed, flags=re.IGNORECASE):
        return True

    # 3. No dangerous scheme detected.
    return False