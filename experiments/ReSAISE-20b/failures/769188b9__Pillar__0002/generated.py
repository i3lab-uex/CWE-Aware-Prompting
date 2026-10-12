import urllib.request
import urllib.error
from hmac import compare_digest

# Example global dictionary of expected signatures.
# In production this would be populated securely, e.g. from a config file or secret store.
DOC_HASHES = {
    # 'https://example.com/doc1.pdf': 'expected_hex_signature',
}

def authenticate_document(resource_url: str, crypto_signature: str) -> bool:
    """
    Verify that a document's cryptographic signature matches the expected value.

    Parameters
    ----------
    resource_url : str
        URL of the document to validate.
    crypto_signature : str
        Cryptographic signature submitted with the document.

    Returns
    -------
    bool
        True if the signature matches the expected value, False otherwise.

    Raises
    ------
    IOError
        If the document at the provided URL is inaccessible.
    """
    # 1. Ensure the resource is reachable
    try:
        with urllib.request.urlopen(resource_url, timeout=5) as response:
            # We don't need the content; just checking accessibility.
            if response.status >= 400:
                raise urllib.error.HTTPError(resource_url, response.status,
                                             "HTTP error", response.headers, None)
    except (urllib.error.URLError, urllib.error.HTTPError) as exc:
        # Wrap the exception to conform to the API contract
        raise IOError(f"Unable to access resource at {resource_url}") from exc

    # 2. Retrieve the expected signature for this URL
    expected_sig = DOC_HASHES.get(resource_url)
    if expected_sig is None:
        # If we have no record for the URL, treat it as a failure
        return False

    # 3. Compare signatures in constant time to avoid timing attacks
    return compare_digest(expected_sig, crypto_signature)