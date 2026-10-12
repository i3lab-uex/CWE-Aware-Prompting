import re

# Regular expression that matches dangerous URL schemes.
# It is case‑insensitive and allows optional whitespace before the scheme.
# The pattern matches any URL that starts with a known malicious scheme
# (javascript, vbscript, data, mailto, file, ftp, smb, etc.) except for
# safe image data URLs (data:image/*).
_DANGEROUS_SCHEMES_RE = re.compile(
    r"""
    ^\s*                                    # optional leading whitespace
    (?:                                     # non‑capturing group for the scheme
        javascript:|
        vbscript:|
        data:(?!image/).*|                 # any data URI that is not an image
        mailto:|
        file:|
        ftp:|
        smb:|
        //                                   # protocol‑relative URLs (//example.com)
    )
    """,
    re.IGNORECASE | re.VERBOSE
)

def is_malicious_scheme(input_url: str) -> bool:
    """
    Determine whether the provided string contains a potentially malicious
    URL scheme, excluding safe image data URLs.

    Parameters:
        input_url (str): The string to examine.

    Returns:
        bool: True if the string contains a dangerous scheme, False otherwise.
    """
    if not isinstance(input_url, str):
        # If the input is not a string we cannot evaluate it safely.
        return False

    # Strip surrounding whitespace for accurate matching
    url = input_url.strip()

    # If the URL starts with a dangerous scheme, return True
    if _DANGEROUS_SCHEMES_RE.match(url):
        # Special case: allow data:image/* URLs
        if url.lower().startswith("data:image/"):
            return False
        return True

    # No dangerous scheme detected
    return False