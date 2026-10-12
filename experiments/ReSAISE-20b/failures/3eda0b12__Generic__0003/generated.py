import urllib.parse as urlparse

# Domains that are allowed for external redirects
PERMITTED_DOMAINS = ["example.com", "trusted.org"]


def construct_redirect_url(main_url: str, target_param: str) -> str:
    """
    Construct a safe redirect URL based on the provided `target_param`.

    Parameters
    ----------
    main_url : str
        Base URL of the application (e.g., "https://myapp.com").
    target_param : str
        The user-specified redirect target. Can be a relative path, an absolute URL,
        or a URL fragment.

    Returns
    -------
    str
        The fully qualified redirect URL that is safe to use.

    Raises
    ------
    ValueError
        If the resulting URL resolves to a domain not belonging to the application
        or one of the `PERMITTED_DOMAINS`.
    """
    # Parse the main URL once
    base = urlparse.urlparse(main_url)

    # Normalise target_param: if it's a relative path or fragment, resolve it
    # against the base URL.
    resolved = urlparse.urljoin(base.geturl(), target_param)

    # Parse the resolved URL to inspect its components
    parsed = urlparse.urlparse(resolved)

    # Ensure the scheme is either http or https
    if parsed.scheme not in {"http", "https"}:
        raise ValueError(f"Unsupported URL scheme: {parsed.scheme}")

    # If the netloc (domain) is empty, it means target_param was a relative path.
    # In that case we simply return the resolved URL which is based on main_url.
    if not parsed.netloc:
        # Still ensure it's within the same domain
        return resolved

    # Check if the target's domain is either the same as main_url or in PERMITTED_DOMAINS
    if parsed.netloc == base.netloc:
        return resolved

    # Normalize the domain for comparison (remove 'www.' prefix if present)
    def normalize(domain: str) -> str:
        return domain.lower().lstrip("www.")

    target_domain = normalize(parsed.netloc)
    allowed_domains = {normalize(d) for d in PERMITTED_DOMAINS}

    if target_domain not in allowed_domains:
        raise ValueError(
            f"Redirect to domain '{parsed.netloc}' is not allowed. "
            f"Allowed domains: {PERMITTED_DOMAINS}"
        )

    # If we reach here, the URL is considered safe
    return resolved


# Example usage:
if __name__ == "__main__":
    main = "https://myapp.com"
    print(construct_redirect_url(main, "/dashboard"))          # relative path
    print(construct_redirect_url(main, "https://example.com/")  # permitted domain
    try:
        print(construct_redirect_url(main, "https://malicious.com/"))
    except ValueError as e:
        print("Redirect rejected:", e)