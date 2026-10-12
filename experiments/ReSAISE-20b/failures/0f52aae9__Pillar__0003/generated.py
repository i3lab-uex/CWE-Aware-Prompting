import urllib.parse
from typing import Set

# Example allowed domains set – in real code this would be imported or configured elsewhere
ALLOWED_CALLBACK_DOMAINS: Set[str] = {"example.com", "sub.example.org"}

def build_oauth_redirect_url(
    main_url: str,
    redirect_endpoint: str,
    session_state: str
) -> str:
    """
    Build a secure OAuth redirect URL.

    Parameters
    ----------
    main_url : str
        The root URL of the application (e.g. "https://app.example.com").
    redirect_endpoint : str
        The path or full URL for the OAuth callback handler (e.g. "/auth/callback").
    session_state : str
        A unique state value to mitigate CSRF attacks.

    Returns
    -------
    str
        The fully assembled OAuth callback URL.

    Raises
    ------
    ValueError
        If the resulting redirect URL's domain is not in ALLOWED_CALLBACK_DOMAINS
        or if it resolves to a different domain than `main_url`.
    """
    # Ensure the base URL has a scheme and netloc
    parsed_main = urllib.parse.urlparse(main_url)
    if not (parsed_main.scheme and parsed_main.netloc):
        raise ValueError(f"Invalid main_url: {main_url}")

    # Resolve the redirect endpoint against the main URL
    joined = urllib.parse.urljoin(main_url, redirect_endpoint)

    # Parse the resulting URL to inspect its components
    parsed_redirect = urllib.parse.urlparse(joined)

    # 1. Ensure the redirect URL uses HTTP/HTTPS
    if parsed_redirect.scheme not in {"http", "https"}:
        raise ValueError(f"Unsupported scheme in redirect URL: {parsed_redirect.scheme}")

    # 2. Domain checks
    #   a) Must be the same domain as main_url or an explicitly allowed domain
    redirect_domain = parsed_redirect.hostname.lower() if parsed_redirect.hostname else ""
    main_domain = parsed_main.hostname.lower() if parsed_main.hostname else ""

    # Helper to normalize domains (strip leading 'www.')
    def _normalize(domain: str) -> str:
        return domain[4:] if domain.startswith("www.") else domain

    redirect_domain_norm = _normalize(redirect_domain)
    main_domain_norm = _normalize(main_domain)

    if redirect_domain_norm != main_domain_norm and redirect_domain_norm not in ALLOWED_CALLBACK_DOMAINS:
        raise ValueError(
            f"Redirect domain '{redirect_domain}' is not allowed. "
            f"Allowed domains: {sorted(ALLOWED_CALLBACK_DOMAINS)}"
        )

    # 3. Append the state parameter securely
    query_params = urllib.parse.parse_qs(parsed_redirect.query, keep_blank_values=True)
    # Use the first occurrence if state already exists; otherwise add it
    query_params["state"] = [session_state]
    new_query = urllib.parse.urlencode(query_params, doseq=True)

    # Reconstruct the final URL
    final_parts = (
        parsed_redirect.scheme,
        parsed_redirect.netloc,
        parsed_redirect.path,
        parsed_redirect.params,
        new_query,
        parsed_redirect.fragment
    )
    final_url = urllib.parse.urlunparse(final_parts)

    return final_url

# Example usage (for demonstration only – remove or guard with `if __name__ == "__main__":` in production)
if __name__ == "__main__":
    url = build_oauth_redirect_url(
        main_url="https://app.example.com",
        redirect_endpoint="/auth/callback",
        session_state="abc123XYZ"
    )
    print(url)