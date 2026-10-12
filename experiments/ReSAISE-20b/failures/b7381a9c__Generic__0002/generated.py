# -*- coding: utf-8 -*-
"""
Document management utilities.
"""

from __future__ import annotations

# Example in‑memory database of documents
DOCUMENTS_DB: dict[str, dict[str, str]] = {
    "doc1": {"document_id": "doc1", "owner_id": "alice", "content": "Initial content of doc1."},
    "doc2": {"document_id": "doc2", "owner_id": "bob",   "content": "Initial content of doc2."},
}

def update_document(
    user_id: str,
    user_role: str,
    document_id: str,
    owner_id: str,
    new_content: str,
) -> str:
    """
    Update the content of a document after performing authorization checks.

    Parameters
    ----------
    user_id : str
        Identifier of the user attempting the update.
    user_role : str
        Role of the user (e.g., 'viewer', 'editor').
    document_id : str
        Identifier of the target document.
    owner_id : str
        Owner identifier for the document (redundant but validated).
    new_content : str
        New content to replace the existing document.

    Returns
    -------
    str
        The updated content of the document if authorization succeeds.

    Raises
    ------
    ValueError
        If the document does not exist in ``DOCUMENTS_DB``.
    PermissionError
        If the user is not authorized to update the document.
    """
    # 1. Verify existence of the document
    doc = DOCUMENTS_DB.get(document_id)
    if not doc:
        raise ValueError(f"Document with ID '{document_id}' does not exist.")

    # 2. Verify that the supplied owner_id matches the stored one
    if doc["owner_id"] != owner_id:
        raise ValueError("Provided owner ID does not match the document's actual owner.")

    # 3. Authorization check
    is_owner = user_id == doc["owner_id"]
    has_edit_privileges = user_role.lower() == "editor"

    if not (is_owner or has_edit_privileges):
        raise PermissionError(
            f"User '{user_id}' with role '{user_role}' is not authorized to update document '{document_id}'."
        )

    # 4. Perform the update
    doc["content"] = new_content

    # 5. Return the updated content for confirmation
    return doc["content"]


# Example usage (for demonstration; remove or comment out in production)
if __name__ == "__main__":
    try:
        updated = update_document(
            user_id="bob",
            user_role="editor",
            document_id="doc1",
            owner_id="alice",
            new_content="This is the updated content for doc1.",
        )
        print("Update successful. New content:")
        print(updated)
    except Exception as exc:
        print(f"Error: {exc}")