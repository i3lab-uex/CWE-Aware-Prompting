import urllib.request
import urllib.error
import hmac

# Global dictionary mapping document URLs to their expected signatures.
DOC_SIGNATURES = {
    # Example entries
    "https://example.com/docs/contract.pdf": "a1b2c3d4e5f6g7h8i9j0",
    "https://example.com/docs/report.pdf":   "0j9i8h7g6f5e4d3c2b1a",
}

def validate_document(file_url: str, sign: str) -> bool:
    """
    Verify that the provided cryptographic signature matches the expected
    signature for a document located at *file_url*.

    Parameters:
        file_url (str): URL of the remote document.
        sign (str): Signature supplied with the document.

    Returns:
        bool: True if the signature matches; False otherwise.

    Raises:
        IOError: If the document cannot be retrieved from *file_url*.
    """
    # Ensure the URL is reachable.  The content itself is not needed for
    # signature verification, but attempting to fetch it guarantees the
    # document is accessible and protects against a scenario where the URL
    # points to an unavailable resource.
    try:
        with urllib.request.urlopen(file_url, timeout=10) as response:
            # Read a small amount to trigger network I/O; we discard the data.
            response.read(1)
    except urllib.error.URLError as exc:
        # Wrap network errors in IOError to match the specification.
        raise IOError(f"Unable to access document at {file_url}") from exc

    # Retrieve the expected signature for this URL.
    expected_sig = DOC_SIGNATURES.get(file_url)
    if expected_sig is None:
        # No known signature for this URL – treat as a mismatch.
        return False

    # Use constant‑time comparison to mitigate timing attacks
    return hmac.compare_digest(sign, expected_sig)