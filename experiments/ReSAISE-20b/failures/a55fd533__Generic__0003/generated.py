import re

# Regular expression to detect dangerous URL schemes.
# It matches strings that start with a scheme such as
# javascript:, vbscript:, data:, etc.  The pattern excludes
# valid image data URLs (data:image/...) by using a negative look‑ahead.
DANGEROUS_SCHEME_REGEX = re.compile(
    r"""
    ^\s*                             # optional leading whitespace
    (?:                              # non‑capturing group for the scheme
        javascript:|
        vbscript:|
        data:                          # match data: but allow only non‑image data
    )
    (?!\s*image/|[^\n\r]*)            # negative look‑ahead for image data URLs
    """,
    re.IGNORECASE | re.VERBOSE,
)

def contains_dangerous_scheme(user_input: str) -> bool:
    """
    Return True if `user_input` contains a dangerous URL scheme
    (e.g., javascript:, vbscript:) and is not an image data URL.
    """
    if not isinstance(user_input, str):
        # If the input is not a string, we cannot reliably inspect it.
        return False

    # Search for any occurrence of the dangerous scheme in the string.
    return bool(DANGEROUS_SCHEME_REGEX.search(user_input))