from typing import Dict

# Sample in‑memory database of documents
DOCUMENTS_DB: Dict[str, Dict[str, str]] = {
    # Example entry:
    # "doc123": {"document_id": "doc123", "owner_id": "user1", "content": "Initial content"},
}

def alter_document(
    operator_id: str,
    operator_role: str,
    doc_id: str,
    doc_owner_id: str,
    updated_content: str
) -> str:
    """
    Modify the content of an existing document if the operator is authorized.

    Parameters
    ----------
    operator_id : str
        ID of the user attempting to modify the document.
    operator_role : str
        Role of the user ('viewer' or 'editor').
    doc_id : str
        Unique identifier for the target document.
    doc_owner_id : str
        Owner ID stored in the document metadata (redundant check).
    updated_content : str
        New content to replace the current document content.

    Returns
    -------
    str
        The updated document content.

    Raises
    ------
    PermissionError
        If the operator is not an editor or does not own the document.
    KeyError
        If the specified `doc_id` does not exist in DOCUMENTS_DB.
    """

    # Validate that the document exists
    if doc_id not in DOCUMENTS_DB:
        raise KeyError(f"Document with ID '{doc_id}' does not exist.")

    document = DOCUMENTS_DB[doc_id]

    # Check that the provided owner ID matches the stored one
    if document.get("owner_id") != doc_owner_id:
        raise ValueError("Provided owner ID does not match the document's actual owner.")

    # Only editors are allowed to modify documents
    if operator_role.lower() != "editor":
        raise PermissionError("Insufficient permissions: only editors can modify documents.")

    # Optional: Ensure the operator is either the owner or an editor
    if operator_id != document.get("owner_id") and operator_role.lower() != "editor":
        raise PermissionError("Insufficient permissions: you are not the document owner.")

    # Perform the update
    document["content"] = updated_content

    return document["content"]