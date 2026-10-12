import re

# Example in‑memory document store.
DOCUMENTS_DB = {
    "doc1": {"document_id": "doc1", "owner_id": "user123", "content": "Original text"},
    # Add more documents as needed.
}

def _is_valid_content(content: str) -> bool:
    """
    Basic content validation to mitigate potential injection or malicious payloads.
    Adjust the regex according to your security policy.
    """
    # Allow alphanumeric, common punctuation and whitespace; reject scripts or HTML tags.
    return bool(re.fullmatch(r"[A-Za-z0-9\s.,!?;:'\"()\-_/]+", content))

def modify_file(
    account_id: str,
    account_role: str,
    file_id: str,
    owner_id: str,
    updated_content: str
) -> str:
    """
    Modify the content of a document if the user is authorized.

    Parameters
    ----------
    account_id : str
        ID of the user attempting to modify.
    account_role : str
        Role of the user ('viewer', 'editor', etc.).
    file_id : str
        ID of the document to modify.
    owner_id : str
        Owner ID provided for reference (should match the document's actual owner).
    updated_content : str
        New content to be stored.

    Returns
    -------
    str
        The updated document content on success.

    Raises
    ------
    ValueError
        If the file does not exist or if content validation fails.
    PermissionError
        If the user lacks authorization to modify the document.
    """
    # 1. Verify existence of the file
    doc = DOCUMENTS_DB.get(file_id)
    if doc is None:
        raise ValueError(f"Document with ID '{file_id}' not found.")

    # 2. Verify owner consistency
    if doc["owner_id"] != owner_id:
        raise ValueError("Provided owner ID does not match document's actual owner.")

    # 3. Authorization check: must be an editor or the owner
    if account_role.lower() != "editor" and account_id != doc["owner_id"]:
        raise PermissionError("User is not authorized to modify this document.")

    # 4. Validate updated content
    if not _is_valid_content(updated_content):
        raise ValueError("Updated content contains disallowed characters or patterns.")

    # 5. Perform the update
    doc["content"] = updated_content

    return doc["content"]