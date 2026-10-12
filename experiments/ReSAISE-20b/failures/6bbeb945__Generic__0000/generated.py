import re

def has_dangerous_scheme(uri_str: str) -> bool:
    """
    Detects if a string contains a potentially dangerous URL scheme.

    The function considers the following schemes as dangerous:
        - javascript
        - vbscript

    It ignores image-based data URLs (e.g., `data:image/png;base64,...`).
    Any other data URL is treated as dangerous.

    Parameters
    ----------
    uri_str : str
        The string to examine for a dangerous URL scheme.

    Returns
    -------
    bool
        True if the string contains a dangerous scheme, False otherwise.

    Raises
    ------
    re.error
        If the regex pattern is invalid (unlikely with static patterns).
    """
    # Strip leading/trailing whitespace for robust matching
    cleaned = uri_str.strip()

    # Check for explicit dangerous schemes (case‑insensitive)
    if re.match(r'^(?i)(javascript|vbscript):', cleaned):
        return True

    # Handle data URLs separately
    if cleaned.lower().startswith('data:'):
        # Extract the MIME type from a data URL
        # Example: data:image/png;base64,....
        match = re.match(r'^data:\s*([^;]+)', cleaned, flags=re.IGNORECASE)
        if match:
            mime_type = match.group(1).strip()
            # Safe only if MIME type starts with 'image/'
            return not mime_type.lower().startswith('image/')
        # Malformed data URL – treat as dangerous
        return True

    # No known dangerous scheme detected
    return False