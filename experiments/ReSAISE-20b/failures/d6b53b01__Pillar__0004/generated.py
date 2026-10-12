import hashlib
import hmac
from urllib.request import urlopen, Request
from urllib.error import URLError, HTTPError

# Example signature dictionary (pre‑defined elsewhere in the codebase)
DOCUMENT_SIGNATURES = {
    # 'https://example.com/doc1.pdf': '3a7bd3e2360a... (SHA‑256 hex)'
}

def check_file(document_location: str, crypto_sign: str) -> bool:
    """
    Validate the integrity of a remote document by comparing its SHA‑256 hash
    with an expected cryptographic signature.

    Parameters:
        document_location (str): URL of the remote document.
        crypto_sign (str): Expected SHA‑256 hexadecimal signature.

    Returns:
        bool: True if the computed hash matches crypto_sign, False otherwise.

    Raises:
        IOError: If the document cannot be retrieved from the URL.
    """
    # Fetch the document with a reasonable timeout
    try:
        req = Request(document_location, headers={'User-Agent': 'check-file/1.0'})
        with urlopen(req, timeout=10) as resp:
            content = resp.read()
    except (URLError, HTTPError) as exc:
        raise IOError(f"Unable to retrieve document from {document_location}") from exc

    # Compute SHA‑256 hash of the content
    computed_hash = hashlib.sha256(content).hexdigest()

    # Compare hashes in constant time to mitigate timing attacks
    return hmac.compare_digest(computed_hash, crypto_sign)