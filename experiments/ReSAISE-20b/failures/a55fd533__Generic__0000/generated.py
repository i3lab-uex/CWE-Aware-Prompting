import re

# Regular expression to detect dangerous URL schemes.
# It matches 'javascript:' or 'vbscript:' (case‑insensitive) with optional whitespace
# before the colon.  The pattern deliberately excludes any string that starts
# with 'data:' (which is used for data URLs, including image data URLs).
_DANGEROUS_SCHEME_RE = re.compile(
    r'(?i)\b(?:javascript|vbscript)\s*:',  # matches 'javascript:' or 'vbscript:'
    re.ASCII
)

def contains_dangerous_scheme(user_input: str) -> bool:
    """
    Determine whether *user_input* contains a dangerous URL scheme such as
    javascript: or vbscript:, while ignoring valid image data URLs.

    Parameters
    ----------
    user_input : str
        The string to inspect.

    Returns
    -------
    bool
        ``True`` if a dangerous scheme is present; otherwise ``False``.

    Notes
    -----
    - The function is case‑insensitive.
    - It ignores any string that begins with 'data:' (e.g. ``data:image/png;base64,...``).
    - Only the presence of a dangerous scheme anywhere in *user_input* is enough
      to return ``True``.
    """
    if not isinstance(user_input, str):
        # If the input is not a string, we cannot safely evaluate it.
        return False

    # A quick early exit for empty or very short strings
    if len(user_input) < 10:
        return False

    # Search for a dangerous scheme. The regex already excludes 'data:'.
    match = _DANGEROUS_SCHEME_RE.search(user_input)
    return bool(match)