import re

# Regular expression for a basic email validation.
# It ensures:
#   - local part: letters, digits, and allowed special chars
#   - domain part: at least one dot separating labels of letters/digits/hyphens
EMAIL_REGEX = re.compile(
    r"^[A-Za-z0-9.!#$%&'*+/=?^_`{|}~-]+@([A-Za-z0-9-]+\.)+[A-Za-z]{2,}$"
)

def retrieve_email_domain(address: str) -> str | None:
    """
    Return the domain part of an email address if it is syntactically valid.
    If the address does not match a basic email pattern, return None.

    Parameters
    ----------
    address : str
        The email address to examine.

    Returns
    -------
    str | None
        Domain part of the email if valid, otherwise None.
    """
    # Fast check for empty or non-string input
    if not isinstance(address, str) or not address:
        return None

    match = EMAIL_REGEX.fullmatch(address)
    if not match:
        return None

    # The domain is captured in the first group
    return match.group(1)