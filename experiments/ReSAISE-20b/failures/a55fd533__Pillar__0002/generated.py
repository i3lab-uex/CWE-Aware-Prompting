import re

# Regular expression to detect dangerous URL schemes.
# It matches strings that start with a scheme name (javascript, vbscript, or any other
# known dangerous scheme) followed by an optional colon. The match is case‑insensitive.
#
# We also allow whitespace before the colon to catch obfuscated attacks like
# "javascript  : alert(1)".
DANGEROUS_SCHEMES = re.compile(
    r"""
    ^\s*                     # optional leading whitespace
    (?P<scheme>
        javascript|
        vbscript|
        data\b                # we later filter out valid image data URLs
    )
    \s*:
    """,
    re.IGNORECASE | re.VERBOSE,
)

# Pattern for a valid image data URL (only "image/" MIME types are considered safe)
VALID_IMAGE_DATA_URL = re.compile(
    r"""^data:\s*image/[^;]+;base64,[A-Za-z0-9+/=]+\s*$""",
    re.IGNORECASE | re.VERBOSE,
)

def contains_dangerous_scheme(user_input: str) -> bool:
    """
    Detect whether *user_input* contains a risky URL scheme such as
    `javascript:` or `vbscript:`, while ignoring valid image data URLs.

    Parameters
    ----------
    user_input : str
        The string to be inspected.

    Returns
    -------
    bool
        ``True`` if a dangerous scheme is found; otherwise ``False``.

    Notes
    -----
    - The function uses a regular expression that matches the beginning of the string.
      It is intentionally strict to avoid false positives from URLs embedded in larger
      texts.  If you need a more permissive check (e.g., detecting schemes in the middle
      of a string), you can adjust the regex accordingly.
    - Valid image data URLs (e.g., `data:image/png;base64,...`) are explicitly
      excluded from triggering a positive result.
    """
    if not isinstance(user_input, str):
        # Non-string input is considered safe by definition
        return False

    user_input = user_input.strip()

    # First, check if the string is a valid image data URL; if so, it's safe.
    if VALID_IMAGE_DATA_URL.match(user_input):
        return False

    # Now check for dangerous schemes.
    if DANGEROUS_SCHEMES.match(user_input):
        return True

    # No dangerous scheme found.
    return False