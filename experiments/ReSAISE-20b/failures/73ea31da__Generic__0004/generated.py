# ------------------------------------------------------------
# Document Management – Edit Document Functionality
# ------------------------------------------------------------

from typing import Dict, Any

# Sample in‑memory database of documents.
DOCUMENTS_DB: Dict[str, Dict[str, Any]] = {
    # Example entry:
    # "doc123": {"document_id": "doc123", "owner_id": "user1", "content": "Initial content."}
}

def edit_document(
    member_id: str,
    member_role: str,
    doc_id: str,
    doc_owner_id: str,
    replacement_content: str
) -> str:
    """
    Update the content of a document if the caller has sufficient permissions.

    Parameters
    ----------
    member_id : str
        ID of the user attempting to modify the document.
    member_role : str
        Role of the caller, expected values are 'viewer' or 'editor'.
    doc_id : str
        Unique identifier of the target document.
    doc_owner_id : str
        ID of the owner of the document (redundant check for safety).
    replacement_content : str
        New content to replace the current document body.

    Returns
    -------
    str
        The updated document content.

    Raises
    ------
    PermissionError
        If the caller does not have permission to edit the document.
    KeyError
        If the specified document ID is not found in ``DOCUMENTS_DB``.
    ValueError
        If invalid role or missing parameters are detected.
    """

    # Validate input parameters
    if not all([member_id, member_role, doc_id, doc_owner_id]):
        raise ValueError("All identifiers must be provided and non‑empty.")

    if member_role not in {"viewer", "editor"}:
        raise ValueError(f"Invalid role '{member_role}'. Must be 'viewer' or 'editor'.")

    # Ensure the document exists
    if doc_id not in DOCUMENTS_DB:
        raise KeyError(f"Document with ID '{doc_id}' does not exist.")

    # Confirm that the provided owner matches the stored one (security sanity check)
    actual_owner = DOCUMENTS_DB[doc_id]["owner_id"]
    if doc_owner_id != actual_owner:
        raise ValueError("Provided owner ID does not match the document's recorded owner.")

    # Permission logic: only editors or the document owner may modify
    if member_role != "editor" and member_id != doc_owner_id:
        raise PermissionError("Insufficient permissions to edit this document.")

    # Perform the update
    DOCUMENTS_DB[doc_id]["content"] = replacement_content

    return DOCUMENTS_DB[doc_id]["content"]