import re

def contains_dangerous_scheme(user_input: str) -> bool:
    """
    Detects potentially dangerous URL schemes in the input string, excluding
    legitimate image data URLs.

    Parameters
    ----------
    user_input : str
        The string to inspect for malicious URL schemes.

    Returns
    -------
    bool
        True if a dangerous scheme is found, False otherwise.
    """
    # Compile the regex patterns once for efficiency
    _dangerous_scheme_re = re.compile(
        r"""
        (?i)                    # case‑insensitive
        (?:javascript|vbscript)  # the dangerous schemes we want to block
        \s*                      # optional whitespace
        :                         # followed by a colon
        """,
        re.VERBOSE,
    )

    _data_url_re = re.compile(
        r"""
        (?i)            # case‑insensitive
        data:           # literal 'data:' prefix
        [^;]*?          # any characters until the first ';'
        ;               # semicolon that separates media type and encoding
        """,
        re.VERBOSE,
    )

    # First, look for any dangerous scheme
    if _dangerous_scheme_re.search(user_input):
        return True

    # Then look for data URLs that are *not* image/* schemes
    for match in _data_url_re.finditer(user_input):
        media_type = match.group(0).split(';', 1)[0].lower()
        # The media type is everything after 'data:' and before the ';'
        if not media_type.startswith('image/'):
            return True

    # No dangerous scheme detected
    return False