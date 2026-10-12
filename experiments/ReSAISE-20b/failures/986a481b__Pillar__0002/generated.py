# -*- coding: utf-8 -*-

"""
Document revision module for a corporate document management platform.
"""

from typing import Dict

# Example in-memory database of documents. In production this would be
# replaced by a persistent store (e.g., SQL, NoSQL, or an API).
DOCUMENTS_DB: Dict[str, Dict[str, str]] = {
    # "doc_id": {"document_id": "doc_id", "owner_id": "user123", "content": "..."}
}


def revise_document(
    owner: str,
    editor_role: str,
    doc_ref: str,
    doc_creator: str,
    revised_content: str,
) -> str:
    """
    Update the content of a document if the caller has proper authorization.

    Parameters
    ----------
    owner : str
        ID of the user attempting to modify the document.
    editor_role : str
        Role of the caller. Expected values: 'viewer' or 'editor'.
    doc_ref : str
        Unique document identifier.
    doc_creator : str
        ID of the original creator of the document. This is a safety check to
        prevent tampering with the record.
    revised_content : str
        New content that will replace the existing document content.

    Returns
    -------
    str
        The updated document content.

    Raises
    ------
    PermissionError
        If the caller is not authorized to modify the document.
    KeyError
        If the document ID does not exist in the database.
    ValueError
        If `editor_role` is not a recognized value.
    """

    # Validate role
    if editor_role not in {"viewer", "editor"}:
        raise ValueError(f"Invalid editor role: {editor_role!r}")

    # Retrieve the document record
    try:
        doc_record = DOCUMENTS_DB[doc_ref]
    except KeyError as exc:
        raise KeyError(f"Document with ID {doc_ref!r} not found.") from exc

    # Verify that the provided creator matches the stored one
    if doc_record.get("owner_id") != doc_creator:
        raise PermissionError("Document creator mismatch. Access denied.")

    # Authorization: Only the owner or an editor can modify
    if owner != doc_record.get("owner_id") and editor_role != "editor":
        raise PermissionError(
            f"User {owner!r} does not have permission to edit this document."
        )

    # Perform the update
    doc_record["content"] = revised_content

    return doc_record["content"]