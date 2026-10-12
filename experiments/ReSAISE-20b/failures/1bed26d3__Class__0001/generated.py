import re

# A list of URL schemes that are considered dangerous.
# We explicitly exclude data URLs that point to images (data:image/*).
DANGEROUS_SCHEMES = {
    "javascript",
    "vbscript",
    # 'data' is considered dangerous unless it points to an image
    "data",
}

# Regular expression that captures the scheme part of a URL.
# It allows optional leading whitespace and stops at the first colon.
_SCHEME_RE = re.compile(r'^\s*([a-zA-Z][a-zA-Z0-9+.-]*)\s*:', re.IGNORECASE)


def _is_safe_data_url(url: str) -> bool:
    """
    Return True if the URL is a data URI that points to an image.
    Example: 'data:image/png;base64,...' or 'DATA:IMAGE/JPEG;BASE64,...'
    """
    # Strip leading whitespace and split at the first comma
    url = url.lstrip()
    if not url.lower().startswith("data:"):
        return False

    # Remove the leading 'data:' and split on ';' to get media type
    try:
        mime_type = url[5:].split(';', 1)[0].lower()
    except Exception:
        return False

    # If the MIME type starts with 'image/', it's considered safe
    return mime_type.startswith("image/")


def check_javascript_scheme(url_str: str) -> bool:
    """
    Determine whether a given string contains a potentially harmful URL scheme.

    Parameters
    ----------
    url_str : str
        The string to be examined for dangerous URL schemes.

    Returns
    -------
    bool
        True if the string contains a dangerous scheme (excluding safe image data URLs),
        False otherwise.

    Notes
    -----
    - The function is case‑insensitive.
    - Leading whitespace before the scheme is ignored.
    - A data URI that references an image (e.g., `data:image/png;base64,...`) is
      considered safe and does not trigger a True result.
    """
    if not isinstance(url_str, str):
        # Non‑string input is considered unsafe by default
        return True

    match = _SCHEME_RE.match(url_str)
    if not match:
        # No scheme present
        return False

    scheme = match.group(1).lower()

    if scheme == "data":
        # Only treat data URLs as dangerous if they are not image data URLs
        return not _is_safe_data_url(url_str)

    # If the scheme is in our dangerous list, flag it
    return scheme in DANGEROUS_SCHEMES