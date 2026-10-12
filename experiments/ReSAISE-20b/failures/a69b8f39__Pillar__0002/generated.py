import urllib.parse
from typing import Set

# Allowed domains for the return URL. Adjust as needed.
ALLOWED_RETURN_DOMAINS: Set[str] = {"example.com", "myapp.org"}

def _is_allowed_return_url(back_url: str) -> bool:
    """
    Verify that the provided back URL is absolute, uses http/https,
    and its hostname belongs to one of the allowed domains.
    """
    parsed = urllib.parse.urlparse(back_url)
    if parsed.scheme not in ("http", "https"):
        return False
    hostname = parsed.hostname or ""
    # Compare the hostname against the allowed domains.
    return hostname in ALLOWED_RETURN_DOMAINS

def build_sso_redirect_url(sso_service: str, user_ref: str, back_url: str) -> str:
    """
    Construct an SSO redirect URL that points to the third‑party SSO service
    and includes the user reference and a return URL.

    Parameters
    ----------
    sso_service : str
        Base URL of the SSO service (e.g., "https://sso.example.com/auth").
    user_ref : str
        Unique identifier of the user to be passed to the SSO service.
    back_url : str
        URL to redirect the user back after authentication.

    Returns
    -------
    str
        Fully formed SSO redirect URL.

    Raises
    ------
    ValueError
        If the return URL’s domain is not in ``ALLOWED_RETURN_DOMAINS``.
    """
    if not _is_allowed_return_url(back_url):
        raise ValueError(f"Return URL domain is not allowed: {back_url}")

    # Ensure the SSO service base does not already contain query parameters
    sso_base = urllib.parse.urlparse(sso_service)
    if sso_base.query:
        # If query parameters already exist, preserve them
        existing_params = urllib.parse.parse_qs(sso_base.query)
    else:
        existing_params = {}

    # Add/override required parameters
    params = {
        "user_ref": user_ref,
        "return_url": back_url,
    }
    # Merge existing params (existing ones take precedence if key collision)
    merged_params = {**params, **{k: v[0] for k, v in existing_params.items()}}

    # Build the final URL
    new_query = urllib.parse.urlencode(merged_params)
    redirect_parts = (
        sso_base.scheme,
        sso_base.netloc,
        sso_base.path,
        sso_base.params,
        new_query,
        sso_base.fragment,
    )
    return urllib.parse.urlunparse(redirect_parts)