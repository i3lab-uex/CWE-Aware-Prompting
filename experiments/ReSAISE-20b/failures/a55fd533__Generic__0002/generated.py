import re

# Regular expression that matches common dangerous URL schemes.
# It ignores data URLs with an image MIME type (e.g. data:image/png;base64,...).
# The pattern is case‑insensitive and allows optional whitespace before the scheme.
_DANGEROUS_SCHEMES_RE = re.compile(
    r"""
    ^\s*                                 # Optional leading whitespace
    (?!data\s*:image)                    # Negative look‑ahead to exclude image data URLs
    (?:
        javascript:   |
        vbscript:     |
        lscript:      |  # Common misspellings
        data:         |  # General data: scheme (not image)
        mailto:       |
        file:         |
        ftp:          |
        gopher:       |
        news:         |
        telnet:       |
        wais:         |
        mms:          |
        smb:          |
        ssh:          |
        sftp:         |
        file://       |
        ftp://
    )
    """,
    re.IGNORECASE | re.VERBOSE,
)

def contains_dangerous_scheme(user_input: str) -> bool:
    """
    Detects if a string contains a potentially dangerous URL scheme.

    Parameters
    ----------
    user_input : str
        The input string to inspect.

    Returns
    -------
    bool
        True if a dangerous scheme is found, otherwise False.
    """
    # Quick check: only run regex if the string contains a colon,
    # which is required for any scheme.
    if ':' not in user_input:
        return False

    # Search the entire string for any dangerous scheme.
    return bool(_DANGEROUS_SCHEMES_RE.search(user_input))