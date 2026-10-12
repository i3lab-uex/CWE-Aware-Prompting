import re

# Compile the regex once for efficiency.
# The pattern matches:
#   - "javascript:" or "vbscript:" (case‑insensitive)
#   - any "data:" URL that is NOT an image (i.e. not followed by "image/").
# We use a word boundary to avoid matching parts of other words.
_DANGEROUS_SCHEME_RE = re.compile(
    r'(?i)\b(?:javascript|vbscript|data:(?!image/)[^;]+)',
    flags=re.IGNORECASE
)

def contains_dangerous_scheme(user_input: str) -> bool:
    """
    Return True if *user_input* contains a potentially dangerous URL scheme
    (e.g. javascript:, vbscript:) or a non‑image data URI; otherwise False.

    Parameters
    ----------
    user_input : str
        The string to inspect.

    Returns
    -------
    bool
        True if a dangerous scheme is found, False otherwise.
    """
    if not isinstance(user_input, str):
        # Non‑string inputs are considered safe for this check.
        return False

    # Search the input using the pre‑compiled regex.
    return bool(_DANGEROUS_SCHEME_RE.search(user_input))