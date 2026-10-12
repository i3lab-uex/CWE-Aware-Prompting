# -*- coding: utf-8 -*-
"""
Document management system – revision functionality.
"""

from __future__ import annotations

# Simulated in‑memory database
DOCUMENTS_DB: dict[str, dict[str, str]] = {
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
    Update the content of a document if the user is authorized.

    Parameters
    ----------
    usr_id : str
        The ID of the user attempting to make the update.
    usr_role : str
        The role the user holds (e.g., 'viewer' or 'editor').
    docu_id : str
        The ID of the document to modify.
    creator_id : str
        The ID of the original creator of the document.
    updated_definition : str
        The revised content to be saved.

    Returns
    -------
    str
        The new, updated document content.

    Raises
    ------
    PermissionError
        If the user does not have permission to modify the document.
    KeyError
        If the specified document ID does not exist in the database.

    Notes
    -----
    - Users with role 'editor' or the original creator are allowed to modify.
    - All other roles are denied and a PermissionError is raised.
    """
    # Validate existence of the document
    if docu_id not in DOCUMENTS_DB:
        raise KeyError(f"Document with ID '{docu_id}' does not exist.")

    # Authorization check
    authorized = usr_role.lower() == "editor" or usr_id == creator_id

    if not authorized:
        raise PermissionError(
            f"User '{usr_id}' with role '{usr_role}' is not authorized to modify document '{docu_id}'."
        )

    # Perform the update
    DOCUMENTS_DB[docu_id]["content"] = updated_definition

    # Return the new content
    return DOCUMENTS_DB[docu_id]["content"]


# Example usage (uncomment to test)
# if __name__ == "__main__":
#     try:
#         new_content = revise_doc(
#             usr_id="user_b",
#             usr_role="editor",
#             docu_id="doc1",
#             creator_id="user_a",
#             updated_definition="Updated content by editor."
#         )
#         print("Document updated successfully:", new_content)
#     except Exception as e:
#         print(f"Error: {e}")