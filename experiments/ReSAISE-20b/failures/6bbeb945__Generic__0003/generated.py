import re

# Regular expression that matches common dangerous URL schemes.
# It ignores leading whitespace and is case‑insensitive.
_DANGEROUS_SCHEMES_RE = re.compile(
    r"""(?i)               # case‑insensitive
        ^\s*                # optional leading whitespace
        (?:                 # non‑capturing group for the scheme list
            javascript:
          | vbscript:
          | lgtm:           # some legacy schemes used in old XSS attacks
          | data:           # data scheme is handled separately below
        )
    """,
    re.VERBOSE,
)

# Regular expression to detect image data URLs which are considered safe.
_IMAGE_DATA_URL_RE = re.compile(
    r"""(?i)               # case‑insensitive
        ^\s*data:\s*
        (?:image\/[a-z0-9.+-]+)  # image MIME type
        ;base64:            # base64 encoding (the common form)
    """,
    re.VERBOSE,
)

def has_dangerous_scheme(uri_str: str) -> bool:
    """
    Return True if *uri_str* contains a potentially dangerous URL scheme
    (e.g., javascript:, vbscript:) and is not an image data‑URL.

    Parameters
    ----------
    uri_str : str
        The string to examine.

    Returns
    -------
    bool
        True if a dangerous scheme is present and the string is not an
        image data URL, False otherwise.

    Notes
    -----
    - The function is deliberately conservative: it only checks the very
      beginning of the string for a scheme.  This prevents false positives
      from URLs that contain these substrings later in the path.
    - The data URL check is limited to image MIME types.  Other data URLs
      are still flagged as dangerous.
    """
    if not isinstance(uri_str, str):
        # Non‑string input is considered non‑dangerous for safety.
        return False

    # First, reject obvious image data URLs
    if _IMAGE_DATA_URL_RE.match(uri_str):
        return False

    # Now check for any dangerous scheme at the start of the string
    return bool(_DANGEROUS_SCHEMES_RE.match(uri_str))