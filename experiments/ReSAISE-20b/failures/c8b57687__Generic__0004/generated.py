import xml.sax.saxutils

def create_xml_output(user_input: str, xml_template: str) -> str:
    """
    Safely embed user-provided content into an XML template.

    Parameters
    ----------
    user_input : str
        The input provided by the user that should be inserted into the XML.
    xml_template : str
        The XML structure containing a single placeholder `{user_input}`.

    Returns
    -------
    str
        A fully-formed XML string with the user content inserted.
    """
    # Escape special characters to prevent XML injection attacks
    safe_input = xml.sax.saxutils.escape(user_input, entities={"'": "&apos;", '"': "&quot;"})
    # Insert the escaped content into the template
    return xml_template.format(user_input=safe_input)