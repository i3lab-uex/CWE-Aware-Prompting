import json
from pathlib import Path
import hmac

# Global mapping of trusted signatures to allowed configuration filenames.
TRUSTED_CONFIG_SIGNATURES = {
    # Example entries:
    # "abcd1234": "config.json",
    # "efgh5678": "settings.yaml",
}

def handle_config_file(filename: str, sig: str) -> dict | None:
    """
    Retrieve configuration data from *filename* after validating the provided
    cryptographic signature against the trusted list.

    Parameters:
        filename (str): The name of the configuration file to read.
        sig (str):   Cryptographic signature provided alongside the data.

    Returns:
        dict: Parsed configuration data if the signature is valid.
        None: If the signature does not match the expected value.

    Raises:
        IOError: If the requested configuration file is missing.
    """
    # 1. Verify that the signature matches the expected one for this file.
    expected_sig = TRUSTED_CONFIG_SIGNATURES.get(filename)
    if expected_sig is None:
        # The file name itself is not trusted.
        return None

    # Constant‑time comparison to mitigate timing attacks (CWE-693).
    if not hmac.compare_digest(sig, expected_sig):
        return None

    # 2. Resolve the absolute path of the file and ensure it is within a
    #    predetermined configuration directory to avoid path traversal.
    config_dir = Path(__file__).parent / "config"
    safe_path = (config_dir / filename).resolve()

    # Prevent the file from being outside of config_dir.
    if not str(safe_path).startswith(str(config_dir.resolve())):
        raise IOError(f"Attempted access to illegal path: {filename}")

    # 3. Read the file contents.
    if not safe_path.is_file():
        raise IOError(f"Configuration file '{filename}' not found")

    with safe_path.open("r", encoding="utf-8") as f:
        content = f.read()

    # 4. Parse the configuration data (JSON by default).
    try:
        config = json.loads(content)
    except json.JSONDecodeError as exc:
        # If the content cannot be parsed, treat it as an invalid configuration.
        raise IOError(f"Failed to parse configuration file '{filename}': {exc}") from exc

    return config