import hashlib
import hmac
from urllib.request import urlopen, Request
from urllib.error import URLError, HTTPError

# Example pre‑defined dictionary of authentic signatures (hex digests)
DOCUMENT_SIGNATURES = {
    # 'https://example.com/doc1.pdf': 'a3f5c8e2...',
    # Add actual entries here
}

def check_file(document_location: str, crypto_sign: str) -> bool:
    """
    Verify that the remote document at *document_location* matches the
    provided cryptographic signature *crypto_sign*.

    Parameters:
        document_location (str): URL of the remote document.
        crypto_sign (str): Expected cryptographic signature (hex digest).

    Returns:
        bool: True if the signature matches, False otherwise.

    Raises:
        IOError: If the document cannot be retrieved.
    """
    try:
        # Use a simple GET request; add headers if needed (e.g., User-Agent)
        req = Request(document_location, method='GET')
        with urlopen(req) as resp:
            content = resp.read()
    except (URLError, HTTPError) as exc:
        raise IOError(f"Could not retrieve document: {exc}") from exc

    # Compute SHA‑256 digest of the retrieved content
    computed_digest = hashlib.sha256(content).hexdigest()

    # Constant‑time comparison to avoid timing attacks
    return hmac.compare_digest(computed_digest, crypto_sign)

# Example usage (uncomment and adjust as needed):
# url = "https://example.com/doc1.pdf"
# expected_sig = DOCUMENT_SIGNATURES.get(url)
# if expected_sig and check_file(url, expected_sig):
#     print("Signature verified.")