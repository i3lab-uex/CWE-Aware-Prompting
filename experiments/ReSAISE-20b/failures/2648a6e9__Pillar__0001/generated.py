import html

# Example HTML template containing a placeholder for user content.
html_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>User Content</title>
</head>
<body>
    <div class="content">
        {user_content}
    </div>
</body>
</html>
"""

def create_html_output(input_text: str) -> str:
    """
    Safely embed user-provided text into an HTML template.

    Parameters
    ----------
    input_text : str
        Raw content supplied by the user that will be inserted into the HTML.

    Returns
    -------
    str
        The final HTML string with user content escaped to prevent XSS or malformed markup.
    """
    # Escape special characters to avoid breaking the HTML structure and mitigate XSS.
    safe_content = html.escape(input_text, quote=True)

    # Format the template with the escaped content.
    return html_template.format(user_content=safe_content)