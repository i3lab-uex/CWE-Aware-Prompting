import urllib.request
import urllib.error
from hmac import compare_digest

# Example global dictionary mapping URLs to their expected signatures.
DOCUMENT_SIGNATURES = {
    "https://example.com/doc1.pdf": "sha256:abcd1234...",
    "https://example.org/report.txt": "sha256:efgh5678...",
}

def authenticate_document(url: str, doc_signature: str) -> bool:
    """
    Verify that a document at the given URL matches the provided cryptographic signature.

    Parameters
    ----------
    url : str
        The URL of the document to validate.
    doc_signature : str
        The cryptographic signature supplied for verification.

    Returns
    -------
    bool
        True if the provided signature matches the stored signature for that URL,
        False otherwise.

    Raises
    ------
    IOError
        If the document at the specified URL cannot be retrieved (e.g., 404 or network error).
    """
    # Ensure the document is reachable before attempting signature verification.
    try:
        with urllib.request.urlopen(url) as response:
            # Read a small amount to confirm the document exists.
            # The actual content is not needed for signature validation here.
            response.read(1)
    except urllib.error.HTTPError as e:
        # If the server returns an error (e.g., 404), raise IOError.
        raise IOError(f"Unable to access document at {url}: HTTP status {e.code}") from e
    except urllib.error.URLError as e:
        # Network-related errors.
        raise IOError(f"Unable to access document at {url}: {e.reason}") from e

    # Retrieve the expected signature for this URL.
    expected_signature = DOCUMENT_SIGNATURES.get(url)
    if expected_signature is None:
        # No signature known for this URL; treat as a mismatch.
        return False

    # Use constant-time comparison to mitigate timing attacks (CWE-693).
    return compare_digest(doc_signature, expected_signature)