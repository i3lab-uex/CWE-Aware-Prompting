import re

# Regex to detect dangerous URL schemes (javascript, vbscript, data with non-image MIME types, etc.)
# It ignores safe image data URLs (data:image/*;base64,...)
_DANGEROUS_PROTOCOL_RE = re.compile(
    r"""(?xi)              # case-insensitive, verbose
        ^\s*                # optional leading whitespace
        (?:                 # start of group for scheme detection
            javascript      # javascript:
          | vbscript        # vbscript:
          | data:           # data URLs
              (?!image/ )   # not an image MIME type
          | [a-z][\w+\-.]*  # any other scheme like data, mailto, etc.
        )
        :                    # colon after scheme
    """,
    re.MULTILINE,
)

def verify_javascript_protocol(url_input: str) -> bool:
    """
    Check if the provided string contains a potentially dangerous URL scheme
    such as javascript:, vbscript:, or any data: URL that is not an image.

    Parameters
    ----------
    url_input : str
        The string to examine for dangerous URL schemes.

    Returns
    -------
    bool
        True if a dangerous scheme is detected, False otherwise.
    """
    if not isinstance(url_input, str):
        # Non-string input is considered unsafe by default
        return True

    # Strip leading/trailing whitespace to avoid false negatives
    stripped = url_input.strip()

    # If the string starts with a dangerous scheme, return True
    if _DANGEROUS_PROTOCOL_RE.match(stripped):
        return True

    # No dangerous scheme found
    return False