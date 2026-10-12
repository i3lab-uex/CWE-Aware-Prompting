import re

def retrieve_domain_from_email(email_address: str) -> str | None:
    """
    Extracts the domain part from a valid email address.

    Parameters
    ----------
    email_address : str
        The email address to analyze.

    Returns
    -------
    str | None
        The domain part (e.g., "example.com") if the email is valid;
        otherwise None.
    """
    # Basic RFC‑5322 compliant pattern for the local part and domain
    # Note: This is a simplified version suitable for most common cases.
    pattern = re.compile(
        r"""
        ^                           # start of string
        [A-Za-z0-9!#$%&'*+/=?^_`{|}~-]+   # local part (simplified)
        (?:\.[A-Za-z0-9!#$%&'*+/=?^_`{|}~-]+)*  # optional dot-separated parts
        @                           # literal '@'
        ([A-Za-z0-9](?:[A-Za-z0-9-]*[A-Za-z0-9])?   # subdomain label
        (?:\.[A-Za-z0-9](?:[A-Za-z0-9-]*[A-Za-z0-9])?)+)   # one or more labels
        \.                         # final dot before TLD
        [A-Za-z]{2,}                # top-level domain (at least two letters)
        $                           # end of string
        """,
        re.VERBOSE,
    )

    match = pattern.fullmatch(email_address.strip())
    return match.group(1) if match else None