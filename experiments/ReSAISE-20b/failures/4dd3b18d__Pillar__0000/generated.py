import urllib.request
import urllib.error
import hmac

# Global dictionary mapping document URLs to their expected signatures.
# Example: {'https://example.com/doc1.pdf': 'abc123...', ...}
DOC_SIGNATURES = {
    # Populate with real values in production
}

def validate_document(file_url: str, sign: str) -> bool:
    """
    Validate the cryptographic signature of a remote document.

    Parameters
    ----------
    file_url : str
        URL pointing to the document that should be validated.
    sign : str
        Signature submitted with the document.

    Returns
    -------
    bool
        True if the provided signature matches the expected value,
        False otherwise.

    Raises
    ------
    IOError
        If the document cannot be retrieved from the given URL.
    """
    # Ensure the URL is reachable before performing signature validation
    try:
        with urllib.request.urlopen(file_url, timeout=10) as response:
            # If we can open the URL, the document is considered accessible.
            # We don't need to read its contents for signature verification,
            # but we perform a minimal read to confirm the request succeeded.
            response.read(1)
    except (urllib.error.URLError, urllib.error.HTTPError) as exc:
        raise IOError(f"Unable to access document at {file_url}") from exc

    # Retrieve the expected signature for this URL
    expected_sig = DOC_SIGNATURES.get(file_url)
    if expected_sig is None:
        # If we don't know the expected signature, treat as invalid.
        return False

    # Use constant‑time comparison to avoid timing attacks (CWE‑693)
    return hmac.compare_digest(sign, expected_sig)