import re

# Regular expression that matches common dangerous URL schemes.
# It excludes the `data:image/...` scheme which is a safe data URI for images.
DANGEROUS_SCHEMES_REGEX = re.compile(
    r'''
    \b                                   # word boundary
    (?:                                   # non‑capturing group for scheme list
        javascript:|vbscript:|
        data:(?!image/)[^;]*;            # exclude data:image
    )
    ''',
    re.IGNORECASE | re.VERBOSE,
)

def contains_dangerous_scheme(user_input: str) -> bool:
    """
    Detects whether *user_input* contains a dangerous URL scheme.

    Parameters
    ----------
    user_input : str
        The string to inspect for potentially malicious URL schemes.

    Returns
    -------
    bool
        ``True`` if a dangerous scheme is found (e.g. javascript:, vbscript:)
        and the input does **not** contain a safe image data URL; otherwise
        ``False``.

    Notes
    -----
    The function deliberately ignores the `data:image/...` scheme, which is
    considered safe for embedding image data. All other ``data:`` URIs are
    flagged as dangerous because they can be abused to bypass content‑type
    restrictions.

    The regular expression is case‑insensitive and uses a word boundary to
    avoid false positives inside larger words.
    """
    if not isinstance(user_input, str):
        # Non‑string inputs are considered safe for this check.
        return False

    # Search for any dangerous scheme.  The pattern will not match
    # `data:image/...` URLs.
    return bool(DANGEROUS_SCHEMES_REGEX.search(user_input))