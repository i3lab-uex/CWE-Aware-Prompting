import re

def verify_javascript_protocol(url_input: str) -> bool:
    """
    Detect potentially dangerous URL schemes in *url_input*.

    The function returns ``True`` if the input string starts with a
    suspicious scheme such as ``javascript:``, ``vbscript:`` or any
    ``data:`` URL that is *not* an image data URI.  Image data URLs
    (e.g., ``data:image/png;base64,...``) are considered safe and
    therefore return ``False``.

    Parameters
    ----------
    url_input : str
        The string to examine for dangerous URL schemes.

    Returns
    -------
    bool
        ``True`` if a potentially harmful scheme is detected, otherwise
        ``False``.

    Notes
    -----
    * The check is case‑insensitive.
    * Leading and trailing whitespace are ignored.
    * Only the very first scheme is examined; if a string contains
      multiple URLs, only the initial part is evaluated.
    """
    # Normalize whitespace and make case‑insensitive
    trimmed = url_input.strip()

    # Regular expression to match dangerous schemes at the start.
    #   - javascript:
    #   - vbscript:
    #   - data: (any content)
    pattern = re.compile(r'^(?P<scheme>javascript|vbscript|data)\s*:', re.IGNORECASE)
    match = pattern.match(trimmed)

    if not match:
        # No dangerous scheme detected
        return False

    scheme = match.group('scheme').lower()

    if scheme == 'data':
        # Extract the media type that follows "data:" up to the first ';'
        # or until the end of the string if no semicolon is present.
        media_type_match = re.match(r'^data\s*:\s*([^;]+)', trimmed, re.IGNORECASE)
        if media_type_match:
            media_type = media_type_match.group(1).strip().lower()
            # Allow only image data URLs; everything else is considered dangerous.
            if media_type.startswith('image/'):
                return False
        # If we cannot determine the media type or it's not an image, treat as dangerous.
        return True

    # For javascript and vbscript schemes we flag them as dangerous.
    return True