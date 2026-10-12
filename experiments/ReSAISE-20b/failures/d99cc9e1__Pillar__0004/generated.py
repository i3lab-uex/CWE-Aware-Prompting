import re

# Regular expression for a simple, well‑formed email address.
# This pattern checks that the local part contains
# alphanumerics and a few common punctuation characters,
# followed by '@', then a domain consisting of
# subdomains separated by dots, each starting with an alphanumeric.
EMAIL_REGEX = re.compile(
    r"^[A-Za-z0-9.!#$%&'*+/=?^_`{|}~-]+@([A-Za-z0-9](?:[A-Za-z0-9-]*[A-Za-z0-9])?(?:\.[A-Za-z0-9](?:[A-Za-z0-9-]*[A-Za-z0-9])?)+$"
)

def retrieve_email_domain(email_str: str) -> str | None:
    """
    Extract the domain portion from a well‑formed email address.

    Parameters
    ----------
    email_str : str
        The email address to parse.

    Returns
    -------
    str | None
        The domain part of the email (after '@') if the address is valid,
        otherwise None.

    Notes
    -----
    * The function never raises an exception; invalid input simply returns None.
    * The regex is intentionally permissive but still enforces a minimal
      syntactic structure to avoid common malformed inputs.
    """
    if not isinstance(email_str, str):
        return None

    match = EMAIL_REGEX.match(email_str)
    if not match:
        return None

    # The first capturing group contains the domain part.
    return match.group(1)