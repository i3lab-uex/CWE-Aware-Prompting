from __future__ import annotations

# Simulated in‑memory document store
DOCUMENTS_DB: dict[str, dict[str, str]] = {
    # Example entries (for illustration only)
    "doc_001": {"document_id": "doc_001", "owner_id": "user_a", "content": "Initial content."},
    "doc_002": {"document_id": "doc_002", "owner_id": "user_b", "content": "Another document."},
}


def revise_document(
    owner: str,
    editor_role: str,
    doc_ref: str,
    doc_creator: str,
    revised_content: str,
) -> str:
    """
    Update the content of a document if the caller has sufficient permissions.

    Parameters
    ----------
    owner : str
        The ID of the user attempting to modify the document.
    editor_role : str
        Role of the caller, expected values are 'viewer' or 'editor'.
    doc_ref : str
        Unique identifier of the document to modify.
    doc_creator : str
        The original owner ID stored in the document record.
    revised_content : str
        New content to replace the existing one.

    Returns
    -------
    str
        The updated document content.

    Raises
    ------
    PermissionError
        If the caller does not have permission to modify the document.
    KeyError
        If `doc_ref` is not found in :data:`DOCUMENTS_DB`.
    """
    # Validate role
    if editor_role not in {"viewer", "editor"}:
        raise ValueError("editor_role must be either 'viewer' or 'editor'")

    # Fetch the document
    try:
        doc = DOCUMENTS_DB[doc_ref]
    except KeyError as exc:
        raise KeyError(f"Document '{doc_ref}' not found") from exc

    # Verify that the provided creator matches stored data
    if doc_creator != doc["owner_id"]:
        raise ValueError("Provided document creator does not match stored owner")

    # Authorization check: only the owner or an editor can modify
    if not (owner == doc["owner_id"] or editor_role == "editor"):
        raise PermissionError("User does not have permission to revise this document")

    # Perform the update
    doc["content"] = revised_content

    return doc["content"]