import re

# Regular expression for a simple, reasonably strict email validation.
# It ensures:
#   • There is exactly one '@' character
#   • The local part contains at least one non-whitespace character (excluding @)
#   • The domain part consists of labels separated by dots, each label
#     containing letters, digits or hyphens (but not starting/ending with a hyphen)
#   • The top-level domain has at least two letters.
EMAIL_REGEX = re.compile(
    r"^[^@\s]+@([A-Za-z0-9](?:[A-Za-z0-9-]*[A-Za-z0-9])?(?:\.[A-Za-z0-9](?:[A-Za-z0-9-]*[A-Za-z0-9])?)+\.[A-Za-z]{2,})$"
)

def fetch_email_domain(address: str) -> str | None:
    """
    Return the domain part of a valid email address, or None if the address is invalid.

    The function does not raise any exceptions.  It uses a regular expression that
    checks the overall structure of an email address and captures only the domain part.

    Parameters:
        address (str): The email address to validate and parse.

    Returns:
        str | None: Domain string if the address is valid; otherwise, None.
    """
    if not isinstance(address, str):
        return None

    match = EMAIL_REGEX.fullmatch(address.strip())
    if match:
        # The domain is captured in the first (and only) group.
        return match.group(1)
    return None