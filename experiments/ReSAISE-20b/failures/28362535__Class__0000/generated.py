import re

# Regular expression that matches malicious URL schemes.
#  - javascript: or vbscript: (case‑insensitive)
#  - data: URLs that are *not* image/* (i.e., potential non‑image data URLs)
# The pattern allows optional leading whitespace.
_MALICIOUS_SCHEME_RE = re.compile(
    r"""^\s*                             # optional leading whitespace
        (?:
            (?:javascript|vbscript)       # known dangerous schemes
            \s*:\s*
          |
            data:(?!image/)              # data: scheme not followed by image/
        )
    """,
    re.IGNORECASE | re.VERBOSE
)

def is_malicious_scheme(input_url: str) -> bool:
    """
    Determine whether a string contains a potentially harmful URL scheme.

    Parameters
    ----------
    input_url : str
        The string to examine for dangerous URL schemes.

    Returns
    -------
    bool
        ``True`` if the string contains a malicious scheme (excluding safe
        image data URLs), otherwise ``False``.

    Notes
    -----
    - The function is tolerant to leading whitespace.
    - Only the following schemes are considered malicious:
      * ``javascript:``
      * ``vbscript:``
      * ``data:`` URLs that are not image-based (i.e., the MIME type does
        **not** start with ``image/``).
    - The implementation uses a compiled regular expression for efficiency
      and to avoid re-compilation on every call.

    Raises
    ------
    re.error
        If the underlying regular expression is malformed (unlikely in this
        static code).
    """
    return bool(_MALICIOUS_SCHEME_RE.match(input_url))