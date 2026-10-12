import hashlib
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError

# Global mapping of document URLs to their expected cryptographic signatures.
# Example format: {"https://example.com/doc1.pdf": "a3f9..."}
DOCUMENT_SIGNATURES = {
    # Populate with actual URL → signature mappings
}

def _get_remote_signature(doc_link: str) -> str:
    """
    Retrieve the expected signature for a document from the global mapping.
    Raises KeyError if no entry exists for the given URL.
    """
    return DOCUMENT_SIGNATURES[doc_link]

def _download_document(doc_link: str) -> bytes:
    """
    Attempt to download the document at `doc_link`.
    Raises IOError if the URL cannot be accessed or returns a non-200 status.
    """
    req = Request(doc_link, method="GET")
    try:
        with urlopen(req) as resp:
            if resp.status != 200:
                raise IOError(f"HTTP error {resp.status} for URL: {doc_link}")
            return resp.read()
    except HTTPError as e:
        raise IOError(f"HTTP error {e.code} for URL: {doc_link}") from e
    except URLError as e:
        raise IOError(f"URL error for {doc_link}: {e.reason}") from e

def _compute_signature(data: bytes) -> str:
    """
    Compute a SHA-256 hash of the data and return its hexadecimal representation.
    The cryptographic signature used here is a simple SHA-256 hash for demonstration;
    in real systems, use an appropriate asymmetric algorithm and key.
    """
    return hashlib.sha256(data).hexdigest()

def check_document(doc_link: str, check_signature: str) -> bool:
    """
    Verify that the provided cryptographic signature matches the expected
    signature for the document at `doc_link`.

    Parameters:
        doc_link (str): URL of the remote document.
        check_signature (str): Signature supplied for verification.

    Returns:
        bool: True if signatures match, False otherwise.

    Raises:
        IOError: If the document cannot be retrieved (e.g., 404 or network error).
    """
    # Ensure the document exists by attempting a download.
    data = _download_document(doc_link)

    # Compute signature of the downloaded document.
    computed_sig = _compute_signature(data)

    # Retrieve expected signature from global mapping.
    try:
        expected_sig = _get_remote_signature(doc_link)
    except KeyError as e:
        raise IOError(f"No stored signature for URL: {doc_link}") from e

    # Constant-time comparison to mitigate timing attacks.
    if hashlib.compare_digest(computed_sig, expected_sig) and \
       hashlib.compare_digest(check_signature.lower(), expected_sig.lower()):
        return True
    return False