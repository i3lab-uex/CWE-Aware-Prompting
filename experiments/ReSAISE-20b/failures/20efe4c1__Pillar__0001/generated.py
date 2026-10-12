import re

# Regular expression that matches potentially dangerous URL schemes.
# It ignores data URLs that start with "data:image/" (case-insensitive).
_DANGEROUS_SCHEMES_RE = re.compile(
    r"""
    ^\s*                                   # optional leading whitespace
    (?:                                     # start non-capturing group for scheme
        javascript:                        # 1. javascript:
      | vbscript:                           # 2. vbscript:
      | data:(?!image/)                    # 3. any other data: (but not image)
      | [a-z]+:                             # 4. any other scheme followed by colon
    )
    """,
    re.IGNORECASE | re.VERBOSE,
)

def verify_javascript_protocol(url_input: str) -> bool:
    """
    Determine whether a given string contains a potentially harmful URL scheme.

    Parameters
    ----------
    url_input : str
        The string to examine for possible dangerous URL schemes.

    Returns
    -------
    bool
        ``True`` if the string involves a potentially harmful URL scheme,
        aside from valid image data URLs; ``False`` otherwise.
    """
    if not isinstance(url_input, str):
        # Non-string inputs are considered unsafe by default.
        return True

    # Strip surrounding whitespace and perform the regex match
    if _DANGEROUS_SCHEMES_RE.match(url_input.strip()):
        return True

    return False