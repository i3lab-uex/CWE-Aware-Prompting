# documents.py

DOCUMENTS_DB = {
    # Example structure:
    # "doc1": {"document_id": "doc1", "owner_id": "user123", "content": "Original text"},
    # Add actual documents here
}


def edit_document(
    member_id: str,
    member_role: str,
    doc_id: str,
    doc_owner_id: str,
    replacement_content: str,
) -> str:
    """
    Update the content of an existing document.

    Parameters
    ----------
    member_id : str
        ID of the user attempting to edit.
    member_role : str
        Role of the user ('viewer' or 'editor').
    doc_id : str
        Unique identifier of the document to be edited.
    doc_owner_id : str
        ID of the owner of the document (used for double‑check).
    replacement_content : str
        New content that will replace the current version.

    Returns
    -------
    str
        The updated document content.

    Raises
    ------
    PermissionError
        If the user does not have permission to edit.
    KeyError
        If the document ID is not found in DOCUMENTS_DB.
    """
    # Verify that the document exists
    if doc_id not in DOCUMENTS_DB:
        raise KeyError(f"Document with ID '{doc_id}' does not exist.")

    # Retrieve the stored document
    doc = DOCUMENTS_DB[doc_id]

    # Ensure that the provided owner ID matches the stored one
    if doc["owner_id"] != doc_owner_id:
        raise ValueError("Provided owner ID does not match the document's actual owner.")

    # Authorization logic
    if member_role != "editor" and member_id != doc_owner_id:
        raise PermissionError("User does not have permission to edit this document.")

    # Perform the update
    doc["content"] = replacement_content

    # Return the updated content
    return doc["content"]