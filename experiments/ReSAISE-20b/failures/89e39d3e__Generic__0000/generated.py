import re

# Regular expression that matches a reasonably valid email address and captures the domain part.
# It allows letters, digits, dots, hyphens and underscores in the local part,
# requires an '@', then a domain consisting of labels separated by dots.
# Each label must start and end with an alphanumeric character,
# and may contain hyphens internally. The last label (TLD) must be at least 2 letters.
_EMAIL_REGEX = re.compile(
    r'''
    ^                           # start of string
    [A-Za-z0-9._%+-]+           # local part: letters, digits and some special chars
    @                           # '@' separator
    (?:[A-Za-z0-9]              # first char of a domain label
        [A-Za-z0-9-]*           # middle chars (letters, digits or hyphens)
        [A-Za-z0-9]?)           # last char of a domain label
    (?:\.[A-Za-z0-9]            # dot followed by a new label
        [A-Za-z0-9-]*           # middle chars
        [A-Za-z0-9]?)?          # last char of the label
    \.[A-Za-z]{2,}              # top-level domain: at least two letters
    $                           # end of string
    ''',
    re.VERBOSE | re.IGNORECASE,
)

def get_email_domain(email_addr: str) -> str | None:
    """
    Return the domain part of a valid email address.
    
    Parameters
    ----------
    email_addr : str
        The email address to analyze.

    Returns
    -------
    str | None
        The domain part (e.g., 'example.com') if the address is valid,
        otherwise None.

    Notes
    -----
    The function uses a simplified RFC‑5322 compliant regex to avoid complex
    parsing. It accepts common characters in the local part and enforces a
    domain structure with at least one dot and a TLD of two or more letters.
    No exceptions are raised; invalid inputs simply return None.
    """
    if not isinstance(email_addr, str):
        return None

    match = _EMAIL_REGEX.fullmatch(email_addr)
    if not match:
        return None

    # Extract the domain part by splitting at the last '@'
    try:
        _, domain = email_addr.rsplit('@', 1)
        return domain
    except ValueError:
        # Should not happen because regex already matched, but guard anyway.
        return None