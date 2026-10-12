import re

# Regular expression to detect dangerous URL schemes, excluding valid image data URLs.
# It matches any of the following patterns:
#   - scheme: followed by optional whitespace and a colon
#   - optionally any characters after the colon (lazy match)
# The regex is case‑insensitive and uses a non‑capturing group for the scheme list.
# It also ensures that URLs starting with "data:image/" are ignored by a negative look‑ahead.
_DANGEROUS_SCHEME_RE = re.compile(
    r"""
    ^                              # start of string
    (?!data:image/.*$)             # exclude image data URLs entirely
    (?:
        javascript
      | vbscript
      | lscript
      | msxml
      | wscript
      | ewscript
    )
    \s*:\s*                         # optional whitespace around colon
    """,
    re.IGNORECASE | re.VERBOSE,
)

def detect_js_scheme(url_string: str) -> bool:
    """
    Detects whether a string contains a potentially harmful URL scheme such as
    javascript:, vbscript:, etc., while ignoring valid image data URLs.

    Parameters:
        url_string (str): The string to examine for possible dangerous URL schemes.

    Returns:
        bool: True if the string involves a potentially harmful URL scheme,
              False otherwise.

    Notes:
        - The function uses a compiled regular expression to avoid re-compilation
          overhead on repeated calls.
        - The regex is anchored at the beginning of the string to prevent
          false positives from URLs that contain a dangerous scheme later in the
          path or query string. Adjust if you need to detect schemes anywhere
          within the string.
        - This implementation is intentionally conservative: it only flags a few
          known dangerous schemes. It does not attempt to parse arbitrary URLs.
    """
    if not isinstance(url_string, str):
        return False

    # Strip leading/trailing whitespace to avoid false negatives.
    url_string = url_string.strip()

    return bool(_DANGEROUS_SCHEME_RE.match(url_string))