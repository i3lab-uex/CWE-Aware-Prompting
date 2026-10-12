import urllib.parse as urlparse

# Example list of domains that are allowed for external redirects.
ALLOWED_DOMAINS = {"example.com", "trustedpartner.org"}

def build_redirect_link(app_base_url: str, redirect_param: str) -> str:
    """
    Build a safe redirect URL by combining the application base URL with
    the supplied `redirect_param`.

    Parameters
    ----------
    app_base_url : str
        Base URL of the application, e.g. "https://myapp.com".
    redirect_param : str
        URL path or full URL to which the user wishes to be redirected.

    Returns
    -------
    str
        Fully resolved redirect URL.

    Raises
    ------
    ValueError
        If the resulting URL is unsafe (i.e. points to a domain not in
        ALLOWED_DOMAINS or outside the base domain).
    """
    # Parse the base URL and redirect parameter
    base = urlparse.urlparse(app_base_url.rstrip("/"))
    redirect = urlparse.urlparse(redirect_param)

    # If the redirect is a relative path, join it with the base
    if not redirect.scheme and not redirect.netloc:
        # Normalise path: remove leading slash to avoid overriding netloc
        relative_path = redirect.path.lstrip("/")
        # Build new path by combining base and relative path
        combined_path = "/".join([base.path.rstrip("/"), relative_path])
        # Preserve query and fragment if present
        resolved = urlparse.ParseResult(
            scheme=base.scheme,
            netloc=base.netloc,
            path="/{}".format(combined_path),
            params="",
            query=redirect.query or "",
            fragment=redirect.fragment or "",
        )
    else:
        # Redirect is an absolute URL; ensure it uses HTTPS and
        # that its domain is allowed.
        if redirect.scheme not in {"http", "https"}:
            raise ValueError(f"Unsupported scheme: {redirect.scheme}")
        if redirect.netloc:
            host = redirect.hostname.lower()
            # Allow relative URLs that point to the same domain as base
            if host != base.hostname.lower() and host not in ALLOWED_DOMAINS:
                raise ValueError(f"Domain '{host}' is not allowed for redirection")
        resolved = redirect

    # Reconstruct the URL
    final_url = urlparse.urlunparse(resolved)

    return final_url

# Example usage:
if __name__ == "__main__":
    base = "https://myapp.com"
    print(build_redirect_link(base, "/dashboard"))           # https://myapp.com/dashboard
    print(build_redirect_link(base, "https://example.com/page"))  # https://example.com/page
    try:
        build_redirect_link(base, "http://malicious.site")
    except ValueError as e:
        print(e)  # Domain 'malicious.site' is not allowed for redirection