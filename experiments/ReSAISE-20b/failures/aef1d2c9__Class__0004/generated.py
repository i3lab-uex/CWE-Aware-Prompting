import re

# Regular expression to detect dangerous URL schemes.
#
#   * Matches a scheme followed by ':' (e.g. "javascript:" or "vbscript:").
#   * Allows optional whitespace and a leading "<" (common in HTML attributes).
#   * Excludes data URLs that start with "data:image/..." by using a negative
#     look‑ahead.
#
# The pattern is deliberately simple to avoid excessive backtracking while
# still catching the most common attack vectors.  It is case‑insensitive.
_DANGEROUS_SCHEME_RE = re.compile(
    r"""(?i)                     # case‑insensitive
        ^\s*                      # optional leading whitespace
        (?:<)?                    # optional '<' that can precede a tag attribute
        (?:
            javascript          |   # javascript:
            vbscript             |   # vbscript:
            data:               # we handle this specially below
        )
        \s*:\s*
    """,
    re.VERBOSE,
)

# Regular expression to detect a valid image data URL.
_DATA_IMAGE_RE = re.compile(r'^\s*data\s*:\s*image\/', re.IGNORECASE)


def has_script_scheme(url: str) -> bool:
    """
    Determine whether *url* contains a potentially dangerous URL scheme.

    Parameters
    ----------
    url : str
        The string to inspect.  It may contain HTML attribute values, URLs,
        or other text.

    Returns
    -------
    bool
        ``True`` if a dangerous scheme such as ``javascript:`` or ``vbscript:``
        is present, *excluding* valid image data URLs.  Otherwise ``False``.
    """
    if not isinstance(url, str):
        raise TypeError("url must be a string")

    # Quick reject for data:image URLs
    if _DATA_IMAGE_RE.match(url):
        return False

    # Search for any dangerous scheme
    return bool(_DANGEROUS_SCHEME_RE.search(url))