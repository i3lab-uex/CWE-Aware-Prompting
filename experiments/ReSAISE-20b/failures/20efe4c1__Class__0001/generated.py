import re

# Regular expression that matches a URL scheme at the start of the string.
# It is case‑insensitive and allows optional whitespace before the scheme.
#
# The pattern captures:
#   1. Any alphabetic scheme followed by a colon (e.g., "javascript:", "vbscript:")
#   2. It specifically excludes data URLs that start with "data:image/"
#
# Example matches:
#   javascript:alert(1)
#   vbscript:MsgBox("Hi")
#
# Non‑matches:
#   data:image/png;base64,iVBORw0KGgo...
#   http://example.com
DANGEROUS_SCHEME_RE = re.compile(
    r'''
    ^\s*                                 # Optional leading whitespace
    (?:                                   # Non‑capturing group for the scheme part
        (?:
            javascript | vbscript      # List of dangerous schemes
        )
    )                                    #
    :                                     # Colon separating scheme from the rest
    ''',
    re.IGNORECASE | re.VERBOSE
)

# Regular expression to detect a data URL that is an image.
DATA_IMAGE_RE = re.compile(
    r'''
    ^\s*                                 # Optional leading whitespace
    data:image                           # "data:image" literal
    ''',
    re.IGNORECASE | re.VERBOSE
)

def verify_javascript_protocol(url_input: str) -> bool:
    """
    Determine whether the supplied string contains a potentially harmful URL scheme.

    Parameters
    ----------
    url_input : str
        The string to examine.  It may contain a URL, an HTML attribute value,
        or any arbitrary text.

    Returns
    -------
    bool
        * `True` if the string starts with a dangerous scheme such as
          ``javascript:`` or ``vbscript:``, ignoring image data URLs.
        * `False` otherwise.

    Notes
    -----
    The function treats the input as a raw string; it does not attempt to parse
    HTML or XML.  It only performs a lightweight regular‑expression check.
    This keeps the function fast while still guarding against typical
    script‑injection vectors.

    Example
    -------
    >>> verify_javascript_protocol('javascript:alert(1)')
    True
    >>> verify_javascript_protocol('data:image/png;base64,AAAA')
    False
    """
    if not isinstance(url_input, str):
        # Non‑string input is considered unsafe; however the function
        # intentionally does not raise an exception to keep a simple API.
        return True

    stripped = url_input.strip()

    # If it is an image data URL, it is considered safe.
    if DATA_IMAGE_RE.match(stripped):
        return False

    # Check for dangerous schemes at the beginning of the string.
    if DANGEROUS_SCHEME_RE.match(stripped):
        return True

    return False