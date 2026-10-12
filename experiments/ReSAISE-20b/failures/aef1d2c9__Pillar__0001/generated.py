import re

# Regular expression to detect dangerous URL schemes at the start of a string.
# It allows optional whitespace before the scheme and matches either
# "javascript:" or "vbscript:".  The trailing colon is required to avoid
# false positives like "javascriptish".
_SCRIPT_SCHEME_RE = re.compile(r'^\s*(?:javascript|vbscript)\b[:;]', re.IGNORECASE)

# Regular expression to detect an image data URL (e.g., "data:image/png;base64,...").
_IMAGE_DATA_URL_RE = re.compile(r'^data\s*:\s*image\/', re.IGNORECASE)


def has_script_scheme(url: str) -> bool:
    """
    Determine whether the supplied string contains a potentially dangerous URL scheme.

    Args:
        url: The input string to be inspected for malicious URL schemes.

    Returns:
        True if the string contains a dangerous scheme such as `javascript:` or
        `vbscript:`, excluding valid image data URLs. False otherwise.

    Notes:
        - The function treats leading whitespace as insignificant.
        - Image data URLs (e.g., "data:image/png;base64,...") are considered safe
          and are ignored by this check.
        - The function is intentionally tolerant of minor variations in case
          and whitespace around the scheme delimiter.
    """
    if not isinstance(url, str):
        # Non-string inputs are considered safe (no scheme to inspect).
        return False

    url_stripped = url.strip()

    # Skip image data URLs – they are considered safe.
    if _IMAGE_DATA_URL_RE.match(url_stripped):
        return False

    # Detect dangerous script schemes.
    return bool(_SCRIPT_SCHEME_RE.match(url_stripped))