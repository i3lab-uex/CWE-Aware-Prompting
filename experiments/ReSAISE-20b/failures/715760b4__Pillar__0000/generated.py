import xml.sax.saxutils as saxutils

# XML template with a placeholder for user content.
xml_template = """<?xml version="1.0" encoding="UTF-8"?>
<response>
    <userEntry>{user_entry}</userEntry>
</response>"""

def produce_xml_message(user_entry: str) -> str:
    """
    Embed the given user entry into a predefined XML template, ensuring that
    any special characters are properly escaped to avoid malformed XML or
    injection attacks.

    Parameters:
        user_entry (str): The raw input from the user to be inserted into
                          the XML response.

    Returns:
        str: A well-formed XML string with the escaped user content.
    """
    # Escape special characters to prevent XML injection and ensure well-formedness
    safe_entry = saxutils.escape(user_entry, {"'": "&apos;", "\"": "&quot;"})
    # Format the template with the escaped content
    return xml_template.format(user_entry=safe_entry)