import re

def get_email_domain(addr: str) -> str | None:
    """
    Extract the domain part of an email address using a regular expression.
    
    Parameters
    ----------
    addr : str
        The email address to examine.

    Returns
    -------
    str | None
        The domain part of the email if it is valid, otherwise None.
    """
    # A simple yet reasonably strict pattern for common email addresses:
    #   - local part: one or more non-@ characters
    #   - domain: at least two labels separated by dots, each label containing letters,
    #     digits or hyphens, ending with a top‑level domain of at least two letters.
    pattern = re.compile(r'^[^@]+@([A-Za-z0-9](?:[A-Za-z0-9-]*[A-Za-z0-9])?(?:\.[A-Za-z0-9](?:[A-Za-z0-9-]*[A-Za-z0-9])?)+$')
    
    match = pattern.match(addr)
    if not match:
        return None

    # The entire domain is captured in the first group
    return match.group(1)