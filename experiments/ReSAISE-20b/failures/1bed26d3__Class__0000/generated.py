import re

def check_javascript_scheme(url_str: str) -> bool:
    """
    Detects potentially dangerous URL schemes in a string, excluding safe image-based data URLs.

    Parameters
    ----------
    url_str : str
        The string to inspect for unsafe URL schemes.

    Returns
    -------
    bool
        ``True`` if the string contains a dangerous scheme such as javascript:, vbscript:,
        or a data URL that is not an image. ``False`` otherwise.

    Notes
    -----
    - The function performs a case‑insensitive search for the scheme at the beginning
      of the string, ignoring leading whitespace.
    - A data URL that specifies an image MIME type (e.g. ``data:image/png;base64,``)
      is considered safe and will not trigger a True result.
    - Any malformed input that causes the regex engine to raise an exception will
      propagate as a ``re.error``.

    Examples
    --------
    >>> check_javascript_scheme('  javascript:alert(1)')
    True
    >>> check_javascript_scheme('data:image/png;base64,AAA')
    False
    >>> check_javascript_scheme('vbscript:msgbox(1)')
    True
    """
    # Strip leading whitespace to avoid matching spaces before the scheme.
    trimmed = url_str.lstrip()

    # Pattern for dangerous schemes: javascript, vbscript, data (unless image)
    scheme_pattern = re.compile(
        r'^(?P<scheme>javascript|vbscript|data):',
        re.IGNORECASE
    )

    match = scheme_pattern.match(trimmed)
    if not match:
        return False

    # If the scheme is data:, check if it's an image MIME type.
    if match.group('scheme').lower() == 'data':
        # Extract the part after "data:" up to the first comma.
        data_part = trimmed[5:]  # Skip 'data:'
        mime_type, _, _ = data_part.partition(',')
        # MIME type may include parameters like charset; split on ';'
        mime_type = mime_type.split(';')[0].strip().lower()
        if mime_type.startswith('image/'):
            # Safe image data URL
            return False

    # Any other matched scheme is considered dangerous.
    return True