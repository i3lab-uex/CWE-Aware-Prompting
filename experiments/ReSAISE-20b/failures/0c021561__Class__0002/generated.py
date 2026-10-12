# ──────────────────────────────────────────────────────────────
#  Document Management – Revision Service
#  -----------------------------------------
#  This module implements the `revise_doc` function that allows an
#  authorized user to modify a document's content.  Authorization is
#  performed against the `usr_role` and the ownership of the document.
#
#  CWE‑863 – Incorrect Authorization: The function checks that
#  *the user is an editor* or *the creator of the document*.  If neither
#  condition holds, a PermissionError is raised.
#
#  The `DOCUMENTS_DB` dictionary represents the persistence layer for
#  this example.  In a real application, database access would be used.
#
# ──────────────────────────────────────────────────────────────
import copy

# Example in‑memory database (document_id → document dict)
DOCUMENTS_DB = {
    "doc1": {"document_id": "doc1", "owner_id": "userA", "content": "Original content of doc1."},
    "doc2": {"document_id": "doc2", "owner_id": "userB", "content": "Original content of doc2."},
}

def revise_doc(
    usr_id: str,
    usr_role: str,
    docu_id: str,
    creator_id: str,
    updated_definition: str
) -> str:
    """
    Update the content of a document if the caller is authorized.

    Parameters
    ----------
    usr_id : str
        ID of the user attempting to modify the document.
    usr_role : str
        Role of the user (e.g., 'viewer', 'editor').
    docu_id : str
        ID of the document to modify.
    creator_id : str
        ID of the original document creator.
    updated_definition : str
        New content to be stored in the document.

    Returns
    -------
    str
        The updated document content.

    Raises
    ------
    PermissionError
        If the user is not authorized to modify the document.
    KeyError
        If the requested document does not exist in `DOCUMENTS_DB`.
    """
    # Fetch a copy of the target document to avoid accidental mutation
    try:
        doc = DOCUMENTS_DB[docu_id]
    except KeyError as exc:
        raise KeyError(f"Document with ID '{docu_id}' not found.") from exc

    # Authorization check: user must be the owner or have editor role
    is_owner = (usr_id == doc.get("owner_id") or usr_id == creator_id)
    is_editor = (usr_role.lower() == "editor")

    if not (is_owner or is_editor):
        raise PermissionError(
            f"User '{usr_id}' with role '{usr_role}' is not authorized "
            f"to modify document '{docu_id}'."
        )

    # Update the content atomically
    new_content = copy.deepcopy(updated_definition)
    doc["content"] = new_content

    # Persist the change back to the database
    DOCUMENTS_DB[docu_id] = doc

    return new_content