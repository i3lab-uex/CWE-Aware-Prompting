# ────────────────────────────────────────────────────────────── #
#  Document Management System – Revision Function
# ────────────────────────────────────────────────────────────── #

from typing import Dict

# Sample in‑memory database
DOCUMENTS_DB: Dict[str, Dict[str, str]] = {
    "doc1": {"document_id": "doc1", "owner_id": "userA", "content": "Initial content"},
    # Add more documents as needed
}

def revise_doc(
    usr_id: str,
    usr_role: str,
    docu_id: str,
    creator_id: str,
    updated_definition: str
) -> str:
    """
    Update the content of a document if the user is authorized.

    Parameters
    ----------
    usr_id : str
        The ID of the user attempting to make the update.
    usr_role : str
        Role of the user (e.g., 'viewer', 'editor').
    docu_id : str
        ID of the target document.
    creator_id : str
        ID of the original creator of the document.
    updated_definition : str
        The new content to be saved.

    Returns
    -------
    str
        The updated document content if the operation succeeds.

    Raises
    ------
    PermissionError
        If the user does not have permission to modify the document.
    KeyError
        If the specified document ID is not found in DOCUMENTS_DB.
    """
    # Validate that the document exists
    if docu_id not in DOCUMENTS_DB:
        raise KeyError(f"Document '{docu_id}' does not exist.")

    doc = DOCUMENTS_DB[docu_id]

    # Check that the creator_id matches the stored owner (defensive check)
    if doc["owner_id"] != creator_id:
        raise ValueError("Creator ID does not match document owner.")

    # Authorization logic
    is_owner = usr_id == doc["owner_id"]
    has_editor_privilege = usr_role.lower() == "editor"

    if not (is_owner or has_editor_privilege):
        raise PermissionError("User is not authorized to modify this document.")

    # Perform the update
    doc["content"] = updated_definition

    return doc["content"]

# ────────────────────────────────────────────────────────────── #
# Example usage (commented out)
# try:
#     new_content = revise_doc(
#         usr_id="userB",
#         usr_role="editor",
#         docu_id="doc1",
#         creator_id="userA",
#         updated_definition="Updated content by editor."
#     )
#     print("Document updated:", new_content)
# except Exception as e:
#     print(e)