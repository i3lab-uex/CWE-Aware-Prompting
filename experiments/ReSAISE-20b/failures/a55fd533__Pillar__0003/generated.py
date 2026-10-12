import re

# Regular expression to detect dangerous URL schemes.
# It matches:
#   * "javascript:" or "vbscript:" (case‑insensitive)
#   * any "data:" URL that is NOT an image data URL.
#
# The pattern uses a negative lookahead to exclude valid image data URLs
# (i.e. those that start with "data:image/").
DANGEROUS_SCHEME_RE = re.compile(
    r"""
    (?i)                          # case‑insensitive matching
    \b(?:                         # start of a word boundary, then one of:
        javascript:               #   javascript:
      | vbscript:                 #   vbscript:
      | data:(?!image/)           #   data:  but NOT followed by image/
    )
    """,
    re.VERBOSE,
)


def contains_dangerous_scheme(user_input: str) -> bool:
    """
    Detect whether *user_input* contains a potentially dangerous URL scheme.

    Parameters
    ----------
    user_input : str
        The string to inspect. It may contain HTML, attributes or plain text.

    Returns
    -------
    bool
        ``True`` if a dangerous scheme is found; otherwise ``False``.

    Notes
    -----
    The function deliberately ignores valid image data URLs (e.g. ``data:image/png;base64,...``).
    It does *not* attempt to fully parse or validate the URL; it merely looks for
    suspicious scheme prefixes that are commonly used in XSS attacks.

    Example
    -------
    >>> contains_dangerous_scheme('onclick="javascript:alert(1)"')
    True
    >>> contains_dangerous_scheme('src="data:image/png;base64,iVBORw0KGgo..."')
    False
    """
    # Fast path: empty or non-string input is safe.
    if not user_input:
        return False

    # Search for any dangerous scheme pattern.
    return bool(DANGEROUS_SCHEME_RE.search(user_input))