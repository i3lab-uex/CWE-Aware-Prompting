from typing import Dict

# Sample in‑memory database of documents.
DOCUMENTS_DB: Dict[str, Dict[str, str]] = {
    "doc1": {"document_id": "doc1", "owner_id": "alice", "content": "Initial content of doc1."},
    "doc2": {"document_id": "doc2", "owner_id": "bob",   "content": "Initial content of doc2."},
    # Add more documents as needed.
}

def update_document(
    user_id: str,
    user_role: str,
    document_id: str,
    owner_id: str,
    new_content: str
) -> str:
    """
    Update the content of a document if the caller is authorized.

    Parameters
    ----------
    user_id : str
        The ID of the user attempting to update the document.
    user_role : str
        The role of the user (e.g., 'viewer', 'editor').
    document_id : str
        The ID of the target document.
    owner_id : str
        The declared owner of the document. Must match the stored owner.
    new_content : str
        The new content to write into the document.

    Returns
    -------
    str
        The updated content of the document.

    Raises
    ------
    ValueError
        If the document does not exist in the database.
    PermissionError
        If the user is not authorized to modify the document.
    """
    # 1. Retrieve the document from the database.
    doc = DOCUMENTS_DB.get(document_id)
    if doc is None:
        raise ValueError(f"Document '{document_id}' not found.")

    # 2. Verify that the declared owner matches the stored owner.
    if doc["owner_id"] != owner_id:
        raise PermissionError("Owner ID mismatch. Access denied.")

    # 3. Authorization check: only editors who are the owner may modify.
    if user_role.lower() != "editor" or user_id != owner_id:
        raise PermissionError("User is not authorized to update this document.")

    # 4. Perform the update.
    doc["content"] = new_content

    # 5. Return the updated content for confirmation.
    return doc["content"]