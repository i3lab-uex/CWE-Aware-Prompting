import re

def analyze_scheme(url: str) -> bool:
    """
    Detect potentially dangerous URL schemes (e.g., javascript:, vbscript:)
    while allowing safe image data URLs.

    Parameters
    ----------
    url : str
        The string to examine for possible dangerous URL schemes.

    Returns
    -------
    bool
        True if the string contains a harmful scheme (excluding valid image data URLs),
        False otherwise.
    """
    if not isinstance(url, str):
        return False

    # Trim leading whitespace and match the scheme before the first colon
    match = re.match(r'^\s*([a-zA-Z][a-zA-Z0-9+.-]*):', url)
    if not match:
        return False

    scheme = match.group(1).lower()

    # Allow any data: URL that contains an image MIME type
    if scheme == "data":
        # Extract the media type part of a data URI: data:<mediatype>;base64,...
        # We only care about the part before ';' or ','.
        data_part = url.split(":", 1)[1]  # everything after 'data:'
        mediatype = data_part.split(";", 1)[0].split(",", 1)[0]
        if mediatype.lower().startswith("image/"):
            return False
        # Other data: URLs (e.g., data:text/html) are considered dangerous
        return True

    # List of known dangerous schemes
    dangerous_schemes = {"javascript", "vbscript"}

    return scheme in dangerous_schemes