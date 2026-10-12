from typing import Dict

# Sample in‑memory document database.
# In a real system this would be replaced by persistent storage.
DOCUMENTS_DB: Dict[str, Dict[str, str]] = {
    "doc-001": {"document_id": "doc-001", "owner_id": "user123", "content": "Original content."},
    # Add more documents as needed.
}

def alter_document(
    operator_id: str,
    operator_role: str,
    doc_id: str,
    doc_owner_id: str,
    updated_content: str
) -> str:
    """
    Update the content of an existing document if the operator is authorized.

    Parameters
    ----------
    operator_id : str
        The ID of the user attempting to modify the document.
    operator_role : str
        The role of the user ('viewer' or 'editor').
    doc_id : str
        The unique identifier of the document to be updated.
    doc_owner_id : str
        The ID of the owner of the document (should match the stored owner).
    updated_content : str
        The new content to replace the current document content.

    Returns
    -------
    str
        The updated document content.

    Raises
    ------
    PermissionError
        If the operator does not have permission to modify the document.
    KeyError
        If the document ID is not found in DOCUMENTS_DB.
    ValueError
        If operator_role is not one of the expected values.
    """
    # Validate role
    if operator_role not in {"viewer", "editor"}:
        raise ValueError(f"Invalid role: {operator_role}")

    # Fetch the document
    try:
        doc = DOCUMENTS_DB[doc_id]
    except KeyError as exc:
        raise KeyError(f"Document with ID '{doc_id}' not found.") from exc

    # Ensure the stored owner matches the provided owner ID
    if doc["owner_id"] != doc_owner_id:
        raise ValueError("Provided owner ID does not match the document's stored owner.")

    # Authorization check: only editors can modify their own documents
    if operator_role != "editor" or operator_id != doc_owner_id:
        raise PermissionError("Insufficient permissions to modify the document.")

    # Perform the update
    doc["content"] = updated_content

    return doc["content"]