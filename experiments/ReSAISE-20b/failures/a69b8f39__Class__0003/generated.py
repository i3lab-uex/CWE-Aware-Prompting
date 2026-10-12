import urllib.parse
from typing import Set

# Allowed domains for the back_url to prevent open‑redirect attacks (CWE‑610)
ALLOWED_RETURN_DOMAINS: Set[str] = {"example.com", "app.example.org"}

def build_sso_redirect_url(sso_service: str, user_ref: str, back_url: str) -> str:
    """
    Construct a secure SSO redirect URL.

    Parameters
    ----------
    sso_service : str
        Base URL of the third‑party SSO service.
    user_ref : str
        Unique identifier for the user (e.g., a UUID or username).
    back_url : str
        The URL to redirect the user back to after SSO.

    Returns
    -------
    str
        A fully formed URL that can be used to redirect the user to the SSO service.

    Raises
    ------
    ValueError
        If ``back_url`` points to a domain not in :data:`ALLOWED_RETURN_DOMAINS`.
    """
    # Parse the back URL and ensure it is absolute
    parsed_back = urllib.parse.urlparse(back_url)
    if not parsed_back.scheme or not parsed_back.netloc:
        raise ValueError("back_url must be a full absolute URL")

    # Validate domain against allowed list
    back_domain = parsed_back.hostname or ""
    if back_domain not in ALLOWED_RETURN_DOMAINS:
        raise ValueError(f"Return URL domain '{back_domain}' is not allowed")

    # Build query parameters safely
    query_params = {
        "user_ref": user_ref,
        "return_url": back_url,  # The SSO provider will redirect here after auth
    }
    encoded_params = urllib.parse.urlencode(query_params, safe=":/")

    # Ensure the SSO service URL ends with a slash for proper joining
    sso_service = sso_service.rstrip("/") + "/"

    # Combine base SSO URL with query string
    redirect_url = urllib.parse.urljoin(sso_service, f"?{encoded_params}")

    return redirect_url