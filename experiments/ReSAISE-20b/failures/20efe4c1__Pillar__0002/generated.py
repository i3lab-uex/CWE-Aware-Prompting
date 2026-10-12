import re

def verify_javascript_protocol(url_input: str) -> bool:
    """
    Detects potentially dangerous URL schemes in a string, ignoring valid image data URLs.

    Parameters
    ----------
    url_input : str
        The string to examine for dangerous URL schemes.

    Returns
    -------
    bool
        True if a harmful scheme is detected (javascript, vbscript, or data: not an image).
        False otherwise.

    Notes
    -----
    This function is intentionally conservative: it only checks the very beginning of the string.
    It does not attempt to parse or validate complete URLs beyond this simple prefix check.
    """
    if not isinstance(url_input, str):
        return False

    # Strip leading whitespace for a more tolerant check
    trimmed = url_input.lstrip()

    # Regular expression to detect dangerous schemes at the start.
    #   - javascript: and vbscript: are obvious threats
    #   - data: is allowed only if it does not start with "image/"
    pattern = re.compile(
        r'^(?P<scheme>javascript|vbscript|data)'
        r':',
        re.IGNORECASE
    )

    match = pattern.match(trimmed)
    if not match:
        return False

    # If the scheme is 'data', ensure it does NOT contain an image MIME type.
    if match.group('scheme').lower() == 'data':
        # Grab everything after "data:" and before any semicolon or comma
        data_payload = trimmed[match.end():]
        # The MIME type ends at the first semicolon or comma, if any.
        mime_end = len(data_payload)
        for sep in (';', ','):
            idx = data_payload.find(sep)
            if 0 <= idx < mime_end:
                mime_end = idx
        mime_type = data_payload[:mime_end].strip().lower()
        # If the MIME type starts with 'image/', it is considered safe.
        if mime_type.startswith('image/'):
            return False

    # Any other scheme matched is considered dangerous
    return True