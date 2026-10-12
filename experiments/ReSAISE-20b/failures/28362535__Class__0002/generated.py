import re

# Regular expression to detect potentially dangerous URL schemes.
#   - Matches 'javascript', 'vbscript', 'data' (except image data URLs) and others commonly abused.
#   - Allows optional whitespace before the scheme.
#   - Case‑insensitive and anchored to start of string or after a delimiter (like '<', '(', etc.).
#   - Excludes image data URLs: `data:image/...` is considered safe.
_MALICIOUS_SCHEME_RE = re.compile(
    r"""
    (?:
        # Optional whitespace and delimiters
        [\s<>()"'`]*

        # Scheme part (non‑capturing group)
        (?:
            javascript
          | vbscript
          | data
          | mailto
          | file
          | ftp
          | ldap
          | nfs
          | smb
          | sftp
        )
        \s*:
    )""",
    re.IGNORECASE | re.VERBOSE,
)

def is_malicious_scheme(input_url: str) -> bool:
    """
    Determine whether the given string contains a potentially dangerous URL scheme,
    excluding safe image-based data URLs.

    Parameters
    ----------
    input_url : str
        The string to be examined for dangerous URL schemes.

    Returns
    -------
    bool
        True if a malicious scheme is detected, False otherwise.
    """
    # Quick sanity check: ensure input is a string
    if not isinstance(input_url, str):
        raise TypeError("input_url must be a string")

    # Find the first match of the malicious scheme pattern
    match = _MALICIOUS_SCHEME_RE.search(input_url)
    if not match:
        return False

    # Extract the matched scheme (e.g., 'javascript', 'data', etc.)
    scheme = match.group(0).split(':')[0].strip().lower()

    # Exclude safe image data URLs
    if scheme == 'data':
        # If the data URL is an image, it is considered safe
        # Pattern: data:image/<mime>;base64,...
        if re.match(r'\s*data\s*:image\/', input_url, re.IGNORECASE):
            return False
        # All other data URLs are considered malicious
        return True

    # Any other scheme matched by the regex is considered malicious
    return True