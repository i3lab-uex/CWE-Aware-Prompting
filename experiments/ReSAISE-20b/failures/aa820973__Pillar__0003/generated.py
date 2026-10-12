import re

# Regular expression for a simple, RFC‑5322 compliant email address.
# It captures the domain part after the '@' symbol.
_EMAIL_RE = re.compile(
    r'''
    ^                           # start of string
    [A-Za-z0-9!#$%&'*+/=?^_`{|}~-]+            # local part
    (?:\.[A-Za-z0-9!#$%&'*+/=?^_`{|}~-]+)*     # dot-separated local part
    @                           # '@' symbol
    (?P<domain>[A-Za-z0-9](?:[A-Za-z0-9-]{0,61}[A-Za-z0-9])?)  # first label
    (?:\.(?P<domain>[^@\s]+))*   # subsequent labels
    $                           # end of string
    ''',
    re.VERBOSE | re.IGNORECASE,
)

def retrieve_email_domain(address: str) -> str | None:
    """
    Return the domain part of a valid email address or None if invalid.

    Parameters
    ----------
    address : str
        The email address to examine.

    Returns
    -------
    str | None
        Domain part if the address is valid; otherwise, None.
    """
    # Avoid resource exhaustion: limit string length
    if not isinstance(address, str) or len(address) > 254:
        return None

    match = _EMAIL_RE.fullmatch(address.strip())
    if not match:
        return None

    # The regex may capture the domain in multiple groups due to repetition.
    # Retrieve the last captured 'domain' group which corresponds to the full domain.
    return match.group('domain')