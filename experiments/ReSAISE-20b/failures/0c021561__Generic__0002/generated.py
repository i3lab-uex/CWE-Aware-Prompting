# revu_doc.py

"""
Document revision module.

This module provides a single function `revise_doc` that allows an authorized
user to update the content of a document stored in the global `DOCUMENTS_DB`
dictionary.

Security notes:
- The function verifies that the document exists.
- It checks that the user is either the owner of the document or has an
  'editor' role.
- It ensures that the `creator_id` supplied matches the document's owner to
  guard against tampering.
- The function raises a `PermissionError` when the user is not authorized.

"""

from __future__ import annotations

# Mock database of documents
DOCUMENTS_DB: dict[str, dict] = {
    "doc_001": {"document_id": "doc_001", "owner_id": "user_a", "content": "Initial content."},
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
        The ID of the document's creator.
    updated_definition : str
        The revised content to be saved.

    Returns
    -------
    str
        The new, updated content of the document.

    Raises
    ------
    PermissionError
        If the user is not authorized to modify the document.
    KeyError
        If the specified document does not exist in DOCUMENTS_DB.
    """
    # Retrieve the document from the database
    try:
        doc = DOCUMENTS_DB[docu_id]
    except KeyError as exc:
        raise KeyError(f"Document '{docu_id}' not found.") from exc

    # Verify that the creator ID matches the document's owner
    if doc["owner_id"] != creator_id:
        raise PermissionError("Creator ID mismatch; unauthorized modification attempt.")

    # Authorization logic: user must be the owner or have an editor role
    if usr_id != doc["owner_id"] and usr_role.lower() != "editor":
        raise PermissionError("User does not have permission to modify this document.")

    # Perform the update
    doc["content"] = updated_definition

    # Return the new content for confirmation
    return doc["content"]

# Example usage (uncomment to test):
# if __name__ == "__main__":
#     try:
#         new_content = revise_doc(
#             usr_id="user_b",
#             usr_role="editor",
#             docu_id="doc_001",
#             creator_id="user_a",
#             updated_definition="Updated content by editor."
#         )
#         print("Document updated successfully:", new_content)
#     except Exception as e:
#         print(f"Error: {e}")