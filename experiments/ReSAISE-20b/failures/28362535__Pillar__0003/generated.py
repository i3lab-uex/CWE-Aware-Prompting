import re

def is_malicious_scheme(input_url: str) -> bool:
    """
    Determine whether the supplied URL string contains a potentially malicious
    scheme.  Image-based data URLs (e.g., data:image/png;base64,...) are
    considered safe and will not trigger a True result.

    Parameters:
        input_url (str): The URL string to examine.

    Returns:
        bool: True if a dangerous scheme is detected (excluding safe image data
              URLs), otherwise False.

    Raises:
        re.error: If the regular expression fails to compile or is used
                  incorrectly.
    """
    # Regular expression that captures the scheme (protocol) part of a URL
    #   e.g., "javascript:", "vbscript:", "data:" etc.
    scheme_re = re.compile(r'^\s*([a-z][a-z0-9+.-]*):', re.IGNORECASE)

    match = scheme_re.match(input_url)
    if not match:
        # No scheme found – cannot be malicious by this definition
        return False

    scheme = match.group(1).lower()

    # Dangerous schemes that we want to flag
    dangerous_schemes = {"javascript", "vbscript"}

    # Special handling for data URLs: safe only if the media type starts with
    #   "image/" (e.g., data:image/png;base64,...)
    if scheme == "data":
        # Extract the media type portion (everything before the first ';' or ',')
        after_scheme = input_url[match.end():].lstrip()
        # Find the delimiter that ends the media type
        delim_pos = min(
            (after_scheme.find(";"), after_scheme.find(",")),
            key=lambda x: x if x != -1 else len(after_scheme)
        )
        media_type = after_scheme[:delim_pos].strip().lower()
        if media_type.startswith("image/"):
            return False
        else:
            # Non‑image data URLs are considered dangerous
            return True

    # If the scheme is in the list of known dangerous schemes, flag it
    return scheme in dangerous_schemes