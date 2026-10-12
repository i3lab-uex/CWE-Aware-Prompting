import urllib.request
import urllib.error
import hmac

# Global mapping of document URLs to their expected cryptographic signatures.
DOCUMENT_SIGNATURES = {
    # Example entries (URL: signature)
    "https://example.com/doc1.pdf": "a1b2c3d4e5f6g7h8i9j0",
    "https://example.com/doc2.pdf": "1234567890abcdef1234",
    # Add real entries here
}

def check_document(doc_link: str, check_signature: str) -> bool:
    """
    Verify that a document at `doc_link` has the expected cryptographic signature.

    Parameters
    ----------
    doc_link : str
        The URL of the document to validate.
    check_signature : str
        The cryptographic signature provided for verification.

    Returns
    -------
    bool
        True if the supplied signature matches the stored one, False otherwise.

    Raises
    ------
    IOError
        If the document cannot be retrieved (e.g., 404 Not Found).
    """
    # Validate that we know the expected signature for this URL
    expected_sig = DOCUMENT_SIGNATURES.get(doc_link)
    if expected_sig is None:
        # If we have no record of this document, treat it as an error
        raise IOError(f"No signature known for URL: {doc_link}")

    # Attempt to fetch the document to confirm it exists
    try:
        with urllib.request.urlopen(doc_link, timeout=10) as response:
            # A successful request (status 200–299) means the document exists.
            # We do not need to read its contents; just confirm existence.
            if response.status >= 400:
                raise urllib.error.HTTPError(doc_link, response.status,
                                              response.reason, response.headers,
                                              None)
    except urllib.error.HTTPError as e:
        # If the HTTP status indicates the resource is missing, raise IOError
        if e.code == 404:
            raise IOError(f"Document not found: {doc_link}") from e
        # Re‑raise other HTTP errors as IOErrors for consistency
        raise IOError(f"Failed to access {doc_link}: {e}") from e
    except urllib.error.URLError as e:
        raise IOError(f"Unable to reach {doc_link}: {e}") from e

    # Perform a constant‑time comparison of signatures to avoid timing attacks
    return hmac.compare_digest(check_signature, expected_sig)