import xml.sax.saxutils

def produce_xml_message(user_entry: str) -> str:
    """
    Generate a safe XML response by embedding the user-provided content
    into a predefined template. The function escapes special XML characters
    to prevent injection or malformed output.

    Parameters:
        user_entry (str): The raw user input that will be inserted into the XML.

    Returns:
        str: A complete XML string with the user content safely escaped.
    """
    # Predefined XML template with a placeholder for user data
    xml_template = (
        "<response>\n"
        "  <message>{user_entry}</message>\n"
        "</response>"
    )

    # Escape special XML characters in the user entry
    safe_user_entry = xml.sax.saxutils.escape(user_entry, entities={"'": "&apos;", '"': "&quot;"})

    # Format the template with the escaped user entry
    return xml_template.format(user_entry=safe_user_entry)