import urllib.request
from urllib.error import URLError, HTTPError

# Global dictionary mapping document URLs to their expected cryptographic signatures.
DOC_HASHES = {
    # Example entries:
    # "https://example.com/doc1.pdf": "sha256:abcd1234...",
    # "https://example.com/doc2.pdf": "sha256:efgh5678..."
}

def authenticate_document(resource_url: str, crypto_signature: str) -> bool:
    """
    Verify that the supplied cryptographic signature matches the expected
    signature for a document located at `resource_url`.

    Parameters
    ----------
    resource_url : str
        The URL of the document to validate.
    crypto_signature : str
        The cryptographic signature submitted with the document.

    Returns
    -------
    bool
        True if the signature matches the expected value for the document,
        False otherwise.

    Raises
    ------
    IOError
        If the document at `resource_url` is inaccessible (e.g., network error,
        HTTP 4xx/5xx status).
    """
    # Check that the URL is reachable before consulting the signature table.
    try:
        with urllib.request.urlopen(resource_url) as response:
            # We don't need the content; we just confirm accessibility.
            if response.status >= 400:
                raise IOError(f"Document inaccessible: HTTP {response.status}")
    except (URLError, HTTPError) as exc:
        # Re‑raise as IOError to match the specification.
        raise IOError(f"Unable to access document at {resource_url}") from exc

    # Retrieve the expected signature for this URL, if any.
    expected_signature = DOC_HASHES.get(resource_url)

    # If no entry exists for the URL, treat it as a mismatch.
    if expected_signature is None:
        return False

    # Perform a constant‑time comparison to mitigate timing attacks.
    def _constant_time_compare(a: str, b: str) -> bool:
        if len(a) != len(b):
            return False
        result = 0
        for x, y in zip(a.encode('utf-8'), b.encode('utf-8')):
            result |= x ^ y
        return result == 0

    return _constant_time_compare(crypto_signature, expected_signature)