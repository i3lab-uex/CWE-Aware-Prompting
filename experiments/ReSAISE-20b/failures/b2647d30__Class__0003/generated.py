from typing import Dict

# Example in‑memory database of documents.
DOCUMENTS_DB: Dict[str, Dict[str, str]] = {
    # document_id : { 'document_id': ..., 'owner_id': ..., 'content': ... }
    "doc1": {"document_id": "doc1", "owner_id": "user123", "content": "Initial content."},
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
    Modify the content of an existing document.

    Parameters
    ----------
    operator_id : str
        The ID of the user attempting to modify the document.
    operator_role : str
        Role of the operator; must be 'editor' to modify a document.
    doc_id : str
        Unique identifier of the target document.
    doc_owner_id : str
        Owner ID claimed for the document (used for verification).
    updated_content : str
        New content that will replace the current document content.

    Returns
    -------
    str
        The updated content of the document.

    Raises
    ------
    PermissionError
        If the operator does not have permission to modify the document.
    KeyError
        If the specified document does not exist in the database.
    """
    # 1. Verify that the document exists
    if doc_id not in DOCUMENTS_DB:
        raise KeyError(f"Document '{doc_id}' does not exist.")

    document = DOCUMENTS_DB[doc_id]

    # 2. Validate ownership
    if doc_owner_id != document["owner_id"]:
        raise PermissionError("Provided owner ID does not match the actual document owner.")

    # 3. Validate operator role and identity
    if operator_role != "editor" or operator_id != document["owner_id"]:
        raise PermissionError("Operator is not authorized to modify this document.")

    # 4. Perform the update
    document["content"] = updated_content

    return document["content"]