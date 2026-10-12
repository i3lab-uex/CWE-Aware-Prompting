import urllib.request
import urllib.error
from hmac import compare_digest

# Global dictionary mapping document URLs to their correct signatures.
# Example: DOC_SIGNATURES = {"https://example.com/doc1.pdf": "abc123...", ...}
DOC_SIGNATURES: dict[str, str] = {}

def validate_document(file_url: str, sign: str) -> bool:
    """
    Verify that the supplied cryptographic signature matches the expected
    signature for a document located at `file_url`.

    Parameters:
        file_url (str): URL of the remote document.
        sign (str): Signature supplied with the request.

    Returns:
        bool: True if the signature matches; False otherwise.

    Raises:
        IOError: If the document cannot be accessed (e.g., network error,
                 404, etc.).
    """
    # Ensure the document is reachable
    try:
        with urllib.request.urlopen(file_url, timeout=10) as resp:
            # We don't need the content; just a successful HTTP 200 is enough.
            if resp.status != 200:
                raise IOError(f"Unexpected status code {resp.status} for URL: {file_url}")
    except urllib.error.HTTPError as e:
        raise IOError(f"HTTP error accessing {file_url}: {e}") from e
    except urllib.error.URLError as e:
        raise IOError(f"URL error accessing {file_url}: {e}") from e
    except Exception as e:
        raise IOError(f"Error accessing {file_url}: {e}") from e

    # Retrieve the expected signature
    expected = DOC_SIGNATURES.get(file_url)
    if expected is None:
        # Unknown document; treat as invalid
        return False

    # Compare using a constant‑time comparison to avoid timing attacks
    return compare_digest(sign, expected)