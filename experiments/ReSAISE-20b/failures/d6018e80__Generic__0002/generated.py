import urllib.parse

# Domains that are allowed to receive the redirect after SSO.
ALLOWED_RETURN_DOMAINS = {"example.com", "myapp.org", "trustedsite.net"}

def create_sso_redirect_url(sso_url: str, uid: str, redirect_url: str) -> str:
    """
    Construct an SSO redirect URL that includes the user ID and a return URL.

    Parameters
    ----------
    sso_url : str
        Base URL of the SSO service (e.g. "https://sso.example.com/login").
    uid : str
        Unique identifier of the user.
    redirect_url : str
        URL to which the SSO service should redirect after authentication.

    Returns
    -------
    str
        The fully‑qualified SSO URL with query parameters.

    Raises
    ------
    ValueError
        If the domain of ``redirect_url`` is not in :data:`ALLOWED_RETURN_DOMAINS`.
    """
    # Validate the redirect URL's domain.
    parsed_redirect = urllib.parse.urlparse(redirect_url)
    hostname = parsed_redirect.hostname

    if not hostname:
        raise ValueError("Redirect URL must contain a valid hostname.")

    # Only the registered domain part is checked. Subdomains are allowed
    # if they resolve to an allowed root domain.
    # For simplicity, we compare the hostname directly with the allowed set.
    if hostname not in ALLOWED_RETURN_DOMAINS:
        raise ValueError(
            f"Return domain '{hostname}' is not allowed. "
            f"Allowed domains: {', '.join(sorted(ALLOWED_RETURN_DOMAINS))}"
        )

    # Build query parameters safely.
    query_params = {
        "uid": uid,
        "redirect": redirect_url
    }
    encoded_query = urllib.parse.urlencode(query_params)

    # Ensure that the base SSO URL does not already contain a query string.
    sso_parsed = urllib.parse.urlparse(sso_url)
    if sso_parsed.query:
        # If there are existing parameters, append with '&'.
        new_query = f"{sso_parsed.query}&{encoded_query}"
    else:
        new_query = encoded_query

    # Reconstruct the full SSO URL.
    sso_parts = list(sso_parsed)
    sso_parts[4] = new_query  # index 4 is the query component
    final_url = urllib.parse.urlunparse(sso_parts)

    return final_url