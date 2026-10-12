import urllib.parse

# Domains that are allowed to be used as a return URL.
ALLOWED_RETURN_DOMAINS = {
    "example.com",
    "app.example.org",
    "trusted-domain.net",
}

def create_sso_redirect_url(sso_url: str, uid: str, redirect_url: str) -> str:
    """
    Build a secure SSO redirect URL.

    Parameters
    ----------
    sso_url : str
        Base URL of the SSO service. Must be absolute and use HTTPS.
    uid : str
        Unique identifier of the user to send to the SSO provider.
    redirect_url : str
        Absolute URL to which the user should be returned after authentication.

    Returns
    -------
    str
        Fully formed URL that can be used to redirect the user to the SSO provider.

    Raises
    ------
    ValueError
        If the return URL does not belong to an allowed domain,
        or if any of the URLs are malformed.
    """
    # ---- Validate SSO URL --------------------------------------------------
    sso_parsed = urllib.parse.urlparse(sso_url)
    if not sso_parsed.scheme or not sso_parsed.netloc:
        raise ValueError("sso_url must be a valid absolute URL")
    if sso_parsed.scheme.lower() != "https":
        raise ValueError("sso_url must use HTTPS for security")

    # ---- Validate and normalize redirect URL --------------------------------
    redirect_parsed = urllib.parse.urlparse(redirect_url)
    if not redirect_parsed.scheme or not redirect_parsed.netloc:
        raise ValueError("redirect_url must be a valid absolute URL")
    # Extract domain without port
    domain = redirect_parsed.hostname.lower() if redirect_parsed.hostname else ""
    if domain not in ALLOWED_RETURN_DOMAINS:
        raise ValueError(f"redirect_url domain '{domain}' is not allowed")

    # ---- Merge query parameters --------------------------------------------
    existing_params = dict(urllib.parse.parse_qsl(sso_parsed.query, keep_blank_values=True))
    # Add or overwrite with uid and redirect
    existing_params.update({
        "uid": uid,
        # Ensure the redirect URL is percent‑encoded
        "redirect": redirect_url,
    })
    new_query = urllib.parse.urlencode(existing_params, doseq=True)

    # ---- Reconstruct full SSO URL -----------------------------------------
    new_sso = sso_parsed._replace(query=new_query)
    return urllib.parse.urlunparse(new_sso)

# Example usage (commented out to keep the module importable)
# if __name__ == "__main__":
#     url = create_sso_redirect_url(
#         "https://sso.example.com/login",
#         uid="user123",
#         redirect_url="https://app.example.org/dashboard"
#     )
#     print(url)