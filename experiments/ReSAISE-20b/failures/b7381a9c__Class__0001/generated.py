# update_document.py

from typing import Dict, Any

# Simulated in‑memory database of documents
DOCUMENTS_DB: Dict[str, Dict[str, Any]] = {
    # Example entry:
    # "doc123": {"document_id": "doc123", "owner_id": "userA", "content": "Initial content"}
}


def update_document(
    user_id: str,
    user_role: str,
    document_id: str,
    owner_id: str,          # This parameter is redundant but kept for API compatibility
    new_content: str,
) -> str:
    """
    Update the content of a document if the caller is authorized.

    Parameters
    ----------
    user_id : str
        The ID of the user attempting the update.
    user_role : str
        Role of the user ('viewer', 'editor', etc.).
    document_id : str
        Identifier of the target document.
    owner_id : str
        Owner of the document (supplied for convenience; must match DB entry).
    new_content : str
        The new document content.

    Returns
    -------
    str
        The updated document content.

    Raises
    ------
    ValueError
        If the document does not exist in `DOCUMENTS_DB`.
    PermissionError
        If the user is not authorized to update the document.
    """
    # 1. Validate that the document exists
    doc = DOCUMENTS_DB.get(document_id)
    if not doc:
        raise ValueError(f"Document with ID '{document_id}' does not exist.")

    # 2. Ensure the supplied owner_id matches the stored one (prevents tampering)
    if doc["owner_id"] != owner_id:
        raise PermissionError("Owner ID mismatch; potential tampering detected.")

    # 3. Authorization check: only the owner or an editor may modify
    if user_id != doc["owner_id"] and user_role.lower() != "editor":
        raise PermissionError("User is not authorized to update this document.")

    # 4. Perform the update
    doc["content"] = new_content

    return doc["content"]