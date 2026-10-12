import urllib.request
import hmac

# Global mapping of document URLs to their valid signatures.
DOCUMENT_SIGNATURES = {
    # Example entries – replace with real values as needed
    "https://example.com/docs/report.pdf": "a1b2c3d4e5f6g7h8i9j0",
    "https://example.com/docs/summary.txt": "1234567890abcdef",
}


def check_document(doc_link: str, check_signature: str) -> bool:
    """
    Verify that a document at ``doc_link`` exists and its cryptographic signature
    matches the expected value stored in DOCUMENT_SIGNATURES.

    Parameters
    ----------
    doc_link : str
        URL of the remote document to validate.
    check_signature : str
        Signature supplied for verification.

    Returns
    -------
    bool
        ``True`` if the document exists and signatures match, otherwise ``False``.

    Raises
    ------
    IOError
        If the document cannot be retrieved (HTTP error or unreachable URL).
    """
    # 1. Ensure the resource is reachable using a HEAD request
    try:
        req = urllib.request.Request(doc_link, method="HEAD")
        with urllib.request.urlopen(req) as resp:
            status = resp.getcode()
    except Exception as exc:  # pragma: no cover
        raise IOError(f"Unable to access document at {doc_link}") from exc

    if status != 200:
        raise IOError(f"Document at {doc_link} returned HTTP status {status}")

    # 2. Retrieve the expected signature from the global dictionary
    expected_sig = DOCUMENT_SIGNATURES.get(doc_link)
    if expected_sig is None:
        # No known signature for this document – treat as mismatch
        return False

    # 3. Perform a constant‑time comparison to avoid timing attacks
    return hmac.compare_digest(expected_sig, check_signature)