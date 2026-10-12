# -*- coding: utf-8 -*-

"""
Document Management System – Modify Document

This module provides a single function, `modify_document`, that safely updates
the content of an existing document.  It enforces the following rules:

1. The document must exist in `DOCUMENTS_DB`.
2. Only users with the role ``editor`` are allowed to modify documents.
3. The user must be the owner of the document, or the system can be extended
   to allow admins/other privileged roles.

The function raises a :class:`PermissionError` when the caller is not
authorized to perform the update.  A generic :class:`KeyError` is raised if
the document does not exist.

The implementation follows best practices for security and correctness,
avoiding common pitfalls such as missing authorization checks or
leaking internal state.
"""

from __future__ import annotations

# Example in‑memory database.  In a real system this would be replaced by
# persistent storage (e.g., a database or external service).
DOCUMENTS_DB: dict[str, dict[str, str]] = {
    "doc-001": {"document_id": "doc-001", "owner_id": "user-a", "content": "Initial content A."},
    "doc-002": {"document_id": "doc-002", "owner_id": "user-b", "content": "Initial content B."},
    # ... more documents
}


def modify_document(
    requester_id: str,
    requester_role: str,
    document_identifier: str,
    document_owner_id: str,
    modified_content: str,
) -> str:
    """
    Update the content of an existing document after performing
    authorization checks.

    Parameters
    ----------
    requester_id : str
        ID of the user attempting to modify the document.
    requester_role : str
        Role of the requester.  Expected values are ``'viewer'`` or ``'editor'``.
    document_identifier : str
        Unique identifier of the target document.
    document_owner_id : str
        Owner ID recorded in the database for the target document.
    modified_content : str
        New content that will replace the current version.

    Returns
    -------
    str
        The updated document content.

    Raises
    ------
    KeyError
        If the document with ``document_identifier`` does not exist.
    PermissionError
        If the requester is not an editor or not the owner of the document.
    """
    # 1. Ensure the document exists
    try:
        doc = DOCUMENTS_DB[document_identifier]
    except KeyError as exc:
        raise KeyError(f"Document '{document_identifier}' not found.") from exc

    # 2. Verify that the provided owner ID matches the stored one
    if doc["owner_id"] != document_owner_id:
        raise ValueError(
            f"Provided owner ID '{document_owner_id}' does not match "
            f"the stored owner ID for document '{document_identifier}'."
        )

    # 3. Authorization check
    if requester_role.lower() != "editor":
        raise PermissionError(
            f"User '{requester_id}' with role '{requester_role}' "
            "is not authorized to modify documents."
        )

    if requester_id != doc["owner_id"]:
        raise PermissionError(
            f"User '{requester_id}' is not the owner of document "
            f"'{document_identifier}'."
        )

    # 4. Perform the update
    doc["content"] = modified_content

    # 5. Return the new content (or you could return a status object)
    return doc["content"]


# Example usage
if __name__ == "__main__":
    try:
        new_text = modify_document(
            requester_id="user-a",
            requester_role="editor",
            document_identifier="doc-001",
            document_owner_id="user-a",
            modified_content="Updated content for doc-001.",
        )
        print("Document updated successfully. New content:")
        print(new_text)
    except Exception as exc:
        print(f"Error: {exc}")