import re

# Regular expression for dangerous URL schemes.
#   * Matches any scheme followed by ':' (e.g., "javascript:", "vbscript:")
#   * Excludes data URLs that start with "data:" and contain an image MIME type.
_DANGEROUS_SCHEMES_RE = re.compile(
    r"""
    (?i)                                   # case-insensitive
    ^\s*                                    # optional leading whitespace
    (?!data:image)                          # negative lookahead: not a data image URL
    (?P<scheme>                              # capture the scheme name
        javascript|
        vbscript|
        data|
        lscript|
        wscript|
        file|
        mailto|
        mms|
        ftp|
        http|
        https|
        news|
        nntp
    )
    :                                      # scheme separator
    """,
    re.VERBOSE,
)

def has_script_scheme(url: str) -> bool:
    """
    Detect if the supplied string contains a potentially dangerous URL scheme.

    Parameters
    ----------
    url : str
        The input string to inspect. It may contain a full URL or just the
        scheme part.

    Returns
    -------
    bool
        ``True`` if a dangerous scheme is detected and the URL is not a valid
        image data URI; otherwise ``False``.
    """
    if not isinstance(url, str):
        return False

    # Strip leading/trailing whitespace and normalise the string.
    url = url.strip()

    # Skip empty strings early.
    if not url:
        return False

    # The regex checks for a dangerous scheme at the beginning of the string.
    match = _DANGEROUS_SCHEMES_RE.match(url)
    if not match:
        return False

    # The negative lookahead already excludes data:image URLs.
    # Any other match is considered dangerous.
    return True