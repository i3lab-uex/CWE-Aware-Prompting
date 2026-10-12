import re

def contains_dangerous_scheme(user_input: str) -> bool:
    """
    Detect if a string contains a dangerous URL scheme (e.g., javascript:, vbscript:)
    while ignoring safe image data URLs (data:image/...).

    Parameters
    ----------
    user_input : str
        The input string to inspect.

    Returns
    -------
    bool
        True if a dangerous scheme is present, False otherwise.
    """
    # Normalise input for case‑insensitive matching
    text = user_input.lower()

    # List of schemes considered dangerous for HTML/JS contexts.
    DANGEROUS_SCHEMES = {"javascript", "vbscript", "data"}

    # Regex to find any scheme of the form <scheme>:
    #   - Starts with a letter
    #   - Followed by letters, digits, '+', '-', or '.'
    #   - Ends with a colon
    scheme_pattern = re.compile(r'\b([a-z][a-z0-9+\-.]*):')

    for match in scheme_pattern.finditer(text):
        scheme = match.group(1)

        # Skip non‑dangerous schemes
        if scheme not in DANGEROUS_SCHEMES:
            continue

        # Special handling for data: scheme
        if scheme == "data":
            # Determine the media type that follows the first comma in the data URL
            # Example: data:image/png;base64,...   -> safe
            #          data:text/html,<script>... -> dangerous
            after_scheme = text[match.end():]  # everything after "data:"
            if not after_scheme:
                continue

            # Extract the media type up to first comma or semicolon
            media_type_match = re.match(r'([^;,]+)', after_scheme)
            if not media_type_match:
                continue
            media_type = media_type_match.group(1)

            # If the media type starts with "image/", we consider it safe
            if media_type.startswith("image/"):
                continue

        # Any other scheme in the dangerous list is flagged
        return True

    return False