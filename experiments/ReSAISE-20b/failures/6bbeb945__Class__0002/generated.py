import re

# Regular expression to detect potentially dangerous URL schemes.
# 1. `javascript:` or `vbscript:` (case‑insensitive)
# 2. `data:` URLs that are not image/* schemes
#
# The pattern uses a non‑capturing group for the scheme and
# ensures that `data:image/` is excluded via a negative look‑ahead.
_DANGEROUS_SCHEME_RE = re.compile(
    r"""
    (?i)                    # case‑insensitive matching
    \b                       # word boundary to avoid partial matches
    (?:                      # non‑capturing group for the scheme list
        javascript:          # classic JavaScript URI scheme
      | vbscript:            # VBScript URI scheme
      | data:(?!image/)     # any data: URI that is NOT an image/*
    )
    """,
    re.VERBOSE
)

def has_dangerous_scheme(uri_str: str) -> bool:
    """
    Detect whether a given string contains a potentially dangerous URL scheme.

    Parameters
    ----------
    uri_str : str
        The string to examine for dangerous schemes.  It may contain an entire URL,
        a fragment of it, or just the scheme part.

    Returns
    -------
    bool
        ``True`` if a dangerous scheme is found, otherwise ``False``.

    Notes
    -----
    * The function explicitly ignores `data:image/...` URLs, as these are
      generally safe for embedding images.
    * The detection is performed using a compiled regular expression to avoid
      repeated compilation overhead and to keep the code readable.
    * The function does not raise any custom exceptions; malformed input may
      cause a ``re.error`` if the regular expression is somehow altered.
    """
    return bool(_DANGEROUS_SCHEME_RE.search(uri_str))