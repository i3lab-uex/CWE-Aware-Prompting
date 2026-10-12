from typing import Dict

# Simulated document storage
DOCUMENTS_DB: Dict[str, Dict[str, str]] = {
    "doc1": {"document_id": "doc1", "owner_id": "userA", "content": "Original content of doc1"},
    "doc2": {"document_id": "doc2", "owner_id": "userB", "content": "Original content of doc2"},
    # Add more documents as needed
}


def revise_document(
    owner: str,
    editor_role: str,
    doc_ref: str,
    doc_creator: str,
    revised_content: str,
) -> str:
    """
    Update the content of a document if the user has sufficient permissions.

    Parameters
    ----------
    owner : str
        ID of the user attempting to modify the document.
    editor_role : str
        Role of the user ('viewer' or 'editor').
    doc_ref : str
        Unique ID of the document to modify.
    doc_creator : str
        ID of the original creator of the document.
    revised_content : str
        New content to replace the existing one.

    Returns
    -------
    str
        The updated document content.

    Raises
    ------
    PermissionError
        If the user does not have permission to modify the document.
    KeyError
        If the requested document does not exist in DOCUMENTS_DB.
    """
    # Validate role input
    if editor_role not in {"viewer", "editor"}:
        raise ValueError("editor_role must be either 'viewer' or 'editor'")

    # Ensure the document exists
    if doc_ref not in DOCUMENTS_DB:
        raise KeyError(f"Document '{doc_ref}' does not exist")

    # Permission check: only the owner or users with 'editor' role can modify
    if not (owner == doc_creator or editor_role == "editor"):
        raise PermissionError("User does not have permission to revise this document")

    # Perform the update
    DOCUMENTS_DB[doc_ref]["content"] = revised_content

    # Return the new content
    return DOCUMENTS_DB[doc_ref]["content"]