import xml.sax.saxutils

# Predefined XML template with a placeholder for user content.
xml_template = """<?xml version="1.0" encoding="UTF-8"?>
<response>
    <userInput>{user_entry}</userInput>
</response>"""

def produce_xml_message(user_entry: str) -> str:
    """
    Generate an XML message by inserting the user-provided content
    into a predefined template. The function escapes special XML
    characters to prevent injection attacks.

    Parameters:
        user_entry (str): The input provided by the user that should
                          be embedded in the XML structure.

    Returns:
        str: A fully-formed XML response with the user content
             safely inserted.
    """
    # Escape special characters to prevent malformed XML or injection.
    safe_entry = xml.sax.saxutils.escape(user_entry, entities={"'": "&apos;", "\"": "&quot;"})
    return xml_template.format(user_entry=safe_entry)