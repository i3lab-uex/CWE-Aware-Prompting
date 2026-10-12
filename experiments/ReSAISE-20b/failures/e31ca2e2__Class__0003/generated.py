import hashlib

# Mock database of documents
DOCUMENTS_DB = {
    "doc1": {"document_id": "doc1", "owner_id": "userA", "content": "Original content 1"},
    "doc2": {"document_id": "doc2", "owner_id": "userB", "content": "Original content 2"},
    # Add more documents as needed
}


def _secure_compare(a: str, b: str) -> bool:
    """
    Constant‑time comparison to prevent timing attacks.
    """
    return hashlib.sha256(a.encode()).digest() == hashlib.sha256(b.encode()).digest()


def edit_doc(u_id: str, u_role: str, doc_id: str, doc_owner: str, new_body: str):
    """
    Edit the content of a document if the user is authorized.

    Parameters
    ----------
    u_id : str
        The ID of the user attempting to make the update.
    u_role : str
        Role of the user (e.g., 'viewer', 'editor').
    doc_id : str
        The ID of the document to modify.
    doc_owner : str
        The ID of the document's creator (should match stored owner_id).
    new_body : str
        The revised content to be saved.

    Returns
    -------
    str
        The updated document content if the user is authorized.

    Raises
    ------
    ValueError
        If the document ID does not exist in the system.
    PermissionError
        If the user is not authorized to edit the document.

    Notes
    -----
    * The function performs a strict equality check for role and ownership,
      avoiding the pitfalls of CWE‑863.
    * The `doc_owner` argument is validated against the stored owner_id to
      guard against tampering.
    """
    # Validate that the document exists
    doc = DOCUMENTS_DB.get(doc_id)
    if not doc:
        raise ValueError(f"Document ID '{doc_id}' does not exist.")

    # Verify that the provided owner matches the stored owner
    if not _secure_compare(doc["owner_id"], doc_owner):
        raise PermissionError("Provided owner ID does not match the document's actual owner.")

    # Authorization check: only editors or the owner can edit
    is_owner = _secure_compare(u_id, doc["owner_id"])
    is_editor = _secure_compare(u_role.lower(), "editor")

    if not (is_owner or is_editor):
        raise PermissionError("User does not have permission to edit this document.")

    # Update the content
    doc["content"] = new_body

    return doc["content"]