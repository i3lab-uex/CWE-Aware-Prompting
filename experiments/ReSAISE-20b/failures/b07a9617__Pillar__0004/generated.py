import re

# Regex to allow only printable ASCII characters (space 0x20 – 0x7E)
# and explicitly disallow CR (\r) and LF (\n) to prevent header injection.
_ALLOWED_HEADER_CHARS = re.compile(r'^[\x20-\x7E]+$')

def insert_header_with_sanitization(custom_header_value: str) -> str:
    """
    Insert a user‑supplied value as a custom header after sanitizing it.

    Parameters
    ----------
    custom_header_value : str
        The raw header value supplied by the user.

    Returns
    -------
    str
        A single HTTP header line with a safe value.
    """
    # 1. Remove any stray CR or LF characters that could split the header
    #    line and allow injection of additional headers.
    cleaned_value = custom_header_value.replace('\r', '').replace('\n', '')

    # 2. Validate the cleaned value against allowed characters.
    if not _ALLOWED_HEADER_CHARS.match(cleaned_value):
        # If the value contains disallowed characters, replace it with a
        # safe placeholder.  Using an empty string is the most conservative.
        cleaned_value = ''

    # 3. Construct the final header line.
    return f"X-Custom-Header: {cleaned_value}"