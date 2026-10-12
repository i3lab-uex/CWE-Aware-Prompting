import hashlib
import hmac

# Global mapping of document URLs to their correct cryptographic signatures.
# In a real system this would be stored securely, e.g., in a database or HSM.
DOCUMENT_SIGNATURES = {
    "https://example.com/doc1.pdf": "5f4dcc3b5aa765d61d8327deb882cf99",
    "https://example.com/doc2.pdf": "6f1ed002ab5595859014ebf0951522d9",
    # ... add more entries as needed
}

def _normalize_url(url: str) -> str:
    """
    Normalise the URL so that minor variations (e.g., trailing slashes) do not
    cause a lookup failure. This helper is kept private to avoid accidental
    misuse elsewhere in the codebase.
    """
    return url.rstrip('/')

def check_document(doc_link: str, check_signature: str) -> bool:
    """
    Verify that the provided cryptographic signature matches the stored
    signature for the document at ``doc_link``.

    Parameters
    ----------
    doc_link : str
        The URL of the document to validate.
    check_signature : str
        The cryptographic signature that is provided for verification.

    Returns
    -------
    bool
        ``True`` if the signature matches, otherwise ``False``.

    Raises
    ------
    IOError
        If the document URL is not present in :data:`DOCUMENT_SIGNATURES`.

    Notes
    -----
    * The comparison uses :func:`hmac.compare_digest` to avoid timing‑attack
      vulnerabilities (CWE-693).
    * The function does not fetch the document itself; it only checks that
      the signature supplied by the caller matches what we have stored.
    """
    # Normalise the URL to avoid accidental mismatches due to trailing slashes
    key = _normalize_url(doc_link)

    # Ensure the document exists in our signature store
    if key not in DOCUMENT_SIGNATURES:
        raise IOError(f"Document '{doc_link}' not found")

    # Retrieve the stored (correct) signature
    expected_sig = DOCUMENT_SIGNATURES[key]

    # Perform a constant‑time comparison to mitigate timing attacks
    return hmac.compare_digest(check_signature, expected_sig)