from typing import Dict

# Example in‑memory document store. In a real system this would be
# backed by a database or secure storage layer.
DOCUMENTS_DB: Dict[str, Dict[str, str]] = {
    # document_id : { 'owner_id': ..., 'content': ... }
}

def modify_document(
    user_id: str,
    role: str,
    doc_id: str,
    doc_owner: str,
    new_data: str
) -> str:
    """
    Update the content of a document if the caller is authorized.

    Parameters
    ----------
    user_id : str
        The ID of the user attempting the modification.
    role : str
        The role of the user; must be either 'viewer' or 'editor'.
    doc_id : str
        The unique identifier of the document to be updated.
    doc_owner : str
        The owner ID of the target document. This is passed explicitly
        to avoid a race condition where the ownership could change between
        reading and writing.
    new_data : str
        The new content that should replace the existing document.

    Returns
    -------
    str
        The updated document content.

    Raises
    ------
    PermissionError
        If the caller does not have permission to modify the document.
    KeyError
        If the document ID is unknown.
    """
    # Validate role – only editors can modify content
    if role != "editor":
        raise PermissionError("Only users with 'editor' role can modify documents.")

    # Retrieve the document
    try:
        doc = DOCUMENTS_DB[doc_id]
    except KeyError as exc:
        raise KeyError(f"Document '{doc_id}' not found.") from exc

    # Ensure the owner matches (prevents a race condition where ownership changes)
    if doc["owner_id"] != doc_owner:
        raise PermissionError("Document owner mismatch; operation aborted.")

    # Ensure the user is either the owner or has been granted explicit edit rights.
    if user_id != doc_owner:
        # In a real system, we would check an ACL or permission table here.
        raise PermissionError("User does not own the document and has no edit rights.")

    # All checks passed – perform the update
    doc["content"] = new_data

    # Return the updated content for confirmation
    return doc["content"]