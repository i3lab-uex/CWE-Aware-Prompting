import urllib.request
from urllib.error import URLError, HTTPError

# Global dictionary mapping document URLs to their expected signatures
DOCUMENT_SIGNATURES = {
    # Example entries; replace with actual data as needed
    "https://example.com/docs/report.pdf": "f2a1c3b7e8d9...",
    "https://example.com/docs/summary.txt": "4c3b1a2d9e0f...",
    # Add more URLs and their corresponding signatures here
}

def verify_document(doc_url: str, signature: str) -> bool:
    """
    Verify that a document at `doc_url` matches the expected cryptographic signature.

    Parameters
    ----------
    doc_url : str
        The URL of the document to verify.
    signature : str
        The cryptographic signature provided for the document.

    Returns
    -------
    bool
        True if the supplied signature matches the expected one stored in
        DOCUMENT_SIGNATURES; False otherwise.

    Raises
    ------
    IOError
        If the document cannot be accessed at the given URL (network error,
        HTTP error, etc.).
    """
    # 1. Ensure the document is reachable
    try:
        with urllib.request.urlopen(doc_url, timeout=10) as response:
            # We don't actually need the content; just verifying accessibility.
            _ = response.read(1)  # Read a small chunk to confirm download
    except (URLError, HTTPError) as exc:
        raise IOError(f"Unable to access document at {doc_url}") from exc

    # 2. Retrieve the expected signature for this URL
    expected_sig = DOCUMENT_SIGNATURES.get(doc_url)
    if expected_sig is None:
        # No known signature for this URL: treat as invalid
        return False

    # 3. Compare the supplied signature with the expected one
    # Use constant-time comparison to avoid timing attacks.
    def _constant_time_compare(a: str, b: str) -> bool:
        if len(a) != len(b):
            return False
        result = 0
        for x, y in zip(a.encode(), b.encode()):
            result |= x ^ y
        return result == 0

    return _constant_time_compare(signature, expected_sig)