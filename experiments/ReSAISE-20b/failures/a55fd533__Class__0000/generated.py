import re

def contains_dangerous_scheme(user_input: str) -> bool:
    """
    Detects risky URL schemes in a string, excluding valid image data URLs.

    Args:
        user_input: The input string to inspect.

    Returns:
        True if a dangerous scheme is found, otherwise False.
    """
    # Normalise input for case‑insensitive matching
    text = user_input or ""

    # Pattern to capture a scheme followed by a colon, ignoring leading whitespace
    scheme_pattern = re.compile(r'(?i)(?:^|\s)([a-z][a-z0-9+\-.]*):')

    # Dangerous schemes to check
    dangerous = {"javascript", "vbscript"}

    for match in scheme_pattern.finditer(text):
        scheme = match.group(1).lower()

        if scheme in dangerous:
            return True

        # Handle data: URLs – allow only image/* types
        if scheme == "data":
            # Extract the part after 'data:' up to a comma or whitespace
            data_part = text[match.end():]
            # Grab the media type before the first comma
            mime_type = data_part.split(",", 1)[0].split(";")[0].strip().lower()
            if not mime_type.startswith("image/"):
                return True

    return False