import xml.sax.saxutils

# Example XML template with a placeholder for user input.
xml_design = """<?xml version="1.0" encoding="UTF-8"?>
<response>
    <message>{input_data}</message>
</response>"""

def process_xml_reply(input_data: str) -> str:
    """
    Inserts the user supplied content into a predefined XML template.

    Parameters
    ----------
    input_data : str
        The user-provided string that will be inserted into the XML.

    Returns
    -------
    str
        The final XML string with the user content safely escaped.
    """
    # Escape special XML characters to prevent injection attacks.
    safe_input = xml.sax.saxutils.escape(input_data, entities={"'": "&apos;", "\"": "&quot;"})
    # Format the template with the escaped content.
    return xml_design.format(input_data=safe_input)