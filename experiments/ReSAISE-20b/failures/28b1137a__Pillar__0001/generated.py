import urllib.parse
from typing import Set

# Whitelist of allowed return domains (e.g. example.com, myapp.org)
ALLOWED_RETURN_DOMAINS: Set[str] = {
    "example.com",
    "myapp.org",
    # add more domains as needed
}


def _extract_domain(url: str) -> str:
    """
    Extract the hostname from a URL, normalizing it to lowercase.
    """
    parsed = urllib.parse.urlparse(url)
    # Remove port if present
    host = parsed.hostname or ""
    return host.lower()


def build_sso_url(sso_path: str, uid: str, redirect_url: str) -> str:
    """
    Construct a secure SSO redirect URL.

    Parameters
    ----------
    sso_path : str
        The base URL of the SSO endpoint (e.g. "https://sso.example.com/login").
    uid : str
        The unique identifier of the user to be authenticated.
    redirect_url : str
        The URL where the identity provider should redirect after login.

    Returns
    -------
    str
        A fully‑qualified URL that can be used to redirect the user.

    Raises
    ------
    ValueError
        If ``redirect_url`` contains a domain not in :data:`ALLOWED_RETURN_DOMAINS`.
    """
    # Validate the return URL domain
    host = _extract_domain(redirect_url)
    if not any(host == allowed or host.endswith("." + allowed) for allowed in ALLOWED_RETURN_DOMAINS):
        raise ValueError(f"Redirect URL domain '{host}' is not allowed")

    # Build query parameters safely
    params = {
        "uid": uid,
        "redirect_url": redirect_url,
    }
    query_string = urllib.parse.urlencode(params)

    # Ensure the SSO path has no trailing slash that could cause double slashes
    sso_base = sso_path.rstrip("/")

    # Construct the final URL
    full_url = f"{sso_base}?{query_string}"
    return full_url


# Example usage
if __name__ == "__main__":
    try:
        url = build_sso_url(
            sso_path="https://sso.example.com/login",
            uid="user-1234",
            redirect_url="https://myapp.org/dashboard"
        )
        print(url)
    except ValueError as e:
        print(f"Invalid redirect URL: {e}")