# -*- coding: utf-8 -*-

from typing import Dict

# Example in‑memory document store.
DOCUMENTS_DB: Dict[str, dict] = {
    # 'doc_id': {'document_id': str, 'owner_id': str, 'content': str}
}

def edit_document(
    member_id: str,
    member_role: str,
    doc_id: str,
    doc_owner_id: str,
    replacement_content: str
) -> str:
    """
    Update the content of an existing document if the caller is authorized.

    Parameters
    ----------
    member_id : str
        ID of the user attempting to modify the document.
    member_role : str
        Role of the caller. Expected values are 'viewer' or 'editor'.
    doc_id : str
        Unique identifier of the document to modify.
    doc_owner_id : str
        Owner ID stored in the database for this document.
    replacement_content : str
        New content that will replace the current version.

    Returns
    -------
    str
        The updated document content.

    Raises
    ------
    KeyError
        If the document ID does not exist in ``DOCUMENTS_DB``.
    PermissionError
        If the caller is not an editor or does not own the document.
    """

    # Validate that the document exists
    if doc_id not in DOCUMENTS_DB:
        raise KeyError(f"Document with ID '{doc_id}' does not exist.")

    # Ensure the owner ID matches the stored value to prevent tampering
    stored_doc = DOCUMENTS_DB[doc_id]
    if doc_owner_id != stored_doc.get("owner_id"):
        raise PermissionError("Provided owner ID does not match the document's actual owner.")

    # Authorization check: only editors who are also owners can modify
    if member_role.lower() != "editor" or member_id != doc_owner_id:
        raise PermissionError("Insufficient permissions to edit this document.")

    # Perform the update
    stored_doc["content"] = replacement_content

    return stored_doc["content"]