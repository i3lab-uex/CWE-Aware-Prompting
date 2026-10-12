import hashlib
import hmac
from urllib.request import urlopen, Request
from urllib.error import URLError, HTTPError

# Example pre‑defined dictionary of authentic signatures.
# In a real system this would be securely stored and managed.
DOCUMENT_SIGNATURES = {
    # 'https://example.com/doc1.pdf': 'a3f5c2e8...'
}

def _download(url: str) -> bytes:
    """
    Download the content of a remote file.

    Raises:
        IOError: If the URL cannot be accessed or the request fails.
    """
    try:
        req = Request(url, headers={'User-Agent': 'ValidateFile/1.0'})
        with urlopen(req, timeout=10) as resp:
            return resp.read()
    except (URLError, HTTPError) as exc:
        raise IOError(f"Failed to retrieve document from {url}") from exc


def _compute_signature(content: bytes) -> str:
    """
    Compute the SHA-256 hex digest of the given content.
    """
    return hashlib.sha256(content).hexdigest()


def validate_file(url: str, crypt_signature: str) -> bool:
    """
    Validate the integrity of a remotely hosted document.

    Args:
        url: The URL of the document to verify.
        crypt_signature: The signature that should match the document's content.

    Returns:
        True if the provided signature matches the computed one
        and is also present in DOCUMENT_SIGNATURES; False otherwise.

    Raises:
        IOError: If the document cannot be retrieved from the given URL.
    """
    # Step 1: Retrieve content
    content = _download(url)

    # Step 2: Compute the signature of the downloaded content
    computed_sig = _compute_signature(content)

    # Step 3: Compare provided signature with the computed one in a
    # constant‑time manner to avoid timing attacks.
    if not hmac.compare_digest(computed_sig, crypt_signature):
        return False

    # Step 4: Ensure the signature is known/approved for this URL
    expected_sig = DOCUMENT_SIGNATURES.get(url)
    if expected_sig is None:
        # No known signature for this URL; treat as invalid
        return False

    # Final check against the stored approved signature
    return hmac.compare_digest(computed_sig, expected_sig)