import re

# Regular expression that matches potentially malicious URL schemes.
# It matches common dangerous schemes such as javascript, vbscript,
# data (but only if not an image data URI), and other typical
# protocols that can be abused in XSS contexts.
MALICIOUS_SCHEME_RE = re.compile(
    r"""
    ^\s*                                 # Optional leading whitespace
    (?:
        (?:javascript|vbscript)          # Common XSS schemes
      | data:(?!image/)[^;]+            # Data URIs that are NOT image types
      | [a-z][a-z0-9+\-.]*:             # Any other scheme (e.g., ftp, mailto)
    )
    """,
    re.IGNORECASE | re.VERBOSE
)

def is_malicious_scheme(input_url: str) -> bool:
    """
    Determine whether a string contains a potentially malicious URL scheme,
    excluding safe image-based data URLs.

    Parameters
    ----------
    input_url : str
        The string to be examined for dangerous URL schemes.

    Returns
    -------
    bool
        True if a dangerous scheme is found, False otherwise.
    """
    # Strip leading/trailing whitespace to avoid false positives
    cleaned = input_url.strip()

    # Quick exit if the string is empty or does not contain a colon
    if not cleaned or ':' not in cleaned:
        return False

    # Use the compiled regex to check for a malicious scheme.
    match = MALICIOUS_SCHEME_RE.match(cleaned)
    return bool(match)

# Example usage (uncomment to test):
# if __name__ == "__main__":
#     tests = [
#         "javascript:alert(1)",
#         "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAA...",
#         "data:text/plain;base64,SGVsbG8sIFdvcmxkIQ==",
#         "ftp://example.com/file.txt",
#         "https://example.com"
#     ]
#     for t in tests:
#         print(t, "->", is_malicious_scheme(t))