import requests
import hmac

# Global dictionary mapping document URLs to their valid cryptographic signatures.
DOCUMENT_SIGNATURES = {
    # Example entries
    "https://example.com/doc1.pdf": "a1b2c3d4e5f6g7h8i9j0",
    "https://example.com/doc2.pdf": "1234567890abcdef1234",
    # Add more URLs and their signatures as needed
}

def authenticate_document(url: str, doc_signature: str) -> bool:
    """
    Verify that the supplied cryptographic signature matches the expected
    signature for a document located at ``url``.

    Parameters
    ----------
    url : str
        The URL of the remote document.
    doc_signature : str
        The cryptographic signature supplied for verification.

    Returns
    -------
    bool
        ``True`` if the provided signature matches the stored one,
        otherwise ``False``.

    Raises
    ------
    IOError
        If the document at ``url`` cannot be retrieved (e.g., 404 Not Found).

    Notes
    -----
    * The function performs a constant‑time comparison of signatures using
      ``hmac.compare_digest`` to mitigate timing attacks (CWE‑347).
    * The function does not download the entire document; it only checks
      the signature. If further validation of the content is required,
      that should be performed elsewhere.
    """
    # Check that the URL exists in our known signature mapping
    if url not in DOCUMENT_SIGNATURES:
        raise IOError(f"Document URL '{url}' not found in signature registry")

    # Retrieve the document to ensure it exists on the server
    try:
        response = requests.head(url, allow_redirects=True, timeout=10)
        if response.status_code != 200:
            raise IOError(f"Unable to access document at {url} (status code: {response.status_code})")
    except requests.RequestException as exc:
        raise IOError(f"Error retrieving document at {url}: {exc}") from exc

    # Retrieve the expected signature
    expected_sig = DOCUMENT_SIGNATURES[url]

    # Perform constant‑time comparison to avoid timing side‑channels
    return hmac.compare_digest(doc_signature, expected_sig)