import html

# Example template with a placeholder for user content.
html_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Dynamic Page</title>
</head>
<body>
    {user_content}
</body>
</html>
"""

def build_html_page(page_content: str) -> str:
    """
    Build a complete HTML page by safely inserting user-provided content.

    Parameters
    ----------
    page_content : str
        The dynamic content supplied by the user that will be inserted into the template.

    Returns
    -------
    str
        The final HTML string with the user content properly escaped to prevent injection attacks.
    """
    # Escape any special HTML characters in the user input to avoid
    # injection of malicious tags or attributes.
    safe_content = html.escape(page_content, quote=True)

    # Inject the escaped content into the template.
    final_html = html_template.format(user_content=safe_content)
    return final_html