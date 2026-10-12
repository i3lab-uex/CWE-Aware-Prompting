# -*- coding: utf-8 -*-
"""
Document management helper module.

Provides a single function `revise_doc` that safely updates the content
of a document in the global `DOCUMENTS_DB` dictionary while enforcing
proper access control (CWE-284).
"""

from __future__ import annotations

# Example in‑memory database
DOCUMENTS_DB: dict[str, dict] = {
    "doc1": {"document_id": "doc1", "owner_id": "user_a", "content": "Initial content"},
    # Add more documents as needed
}


def revise_doc(
    usr_id: str,
    usr_role: str,
    docu_id: str,
    creator_id: str,
    updated_definition: str,
) -> str:
    """
    Update the content of a document if the caller is authorized.

    Parameters
    ----------
    usr_id : str
        ID of the user attempting the update.
    usr_role : str
        Role of the user (e.g., 'viewer', 'editor').
    docu_id : str
        ID of the target document.
    creator_id : str
        The original creator's ID (redundant but kept for backward compatibility).
    updated_definition : str
        The new content to store.

    Returns
    -------
    str
        The updated document content.

    Raises
    ------
    KeyError
        If the specified document does not exist.
    PermissionError
        If the user is not authorized to modify the document.
    """
    # 1. Validate that the document exists
    if docu_id not in DOCUMENTS_DB:
        raise KeyError(f"Document '{docu_id}' does not exist.")

    doc = DOCUMENTS_DB[docu_id]

    # 2. Verify that the creator_id matches the stored owner (safety check)
    if doc.get("owner_id") != creator_id:
        # The provided creator_id does not match the actual owner.
        raise PermissionError("Creator ID mismatch – potential tampering detected.")

    # 3. Authorization logic
    is_owner = usr_id == doc.get("owner_id")
    is_editor = usr_role.lower() == "editor"

    if not (is_owner or is_editor):
        raise PermissionError(
            f"User '{usr_id}' with role '{usr_role}' is not authorized to edit document '{docu_id}'."
        )

    # 4. Perform the update
    doc["content"] = updated_definition

    # 5. Return the new content (could also return the whole document if desired)
    return doc["content"]


# Example usage (uncomment to test):
# try:
#     new_content = revise_doc(
#         usr_id="user_b",
#         usr_role="editor",
#         docu_id="doc1",
#         creator_id="user_a",
#         updated_definition="Updated content here."
#     )
#     print("Document updated:", new_content)
# except Exception as exc:
#     print(f"Error: {exc}")