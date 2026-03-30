import re

def parse_markdown(markdown):
    # Rudimentary CommonMark-compatible parser
    lines = markdown.splitlines()
    html = []
    list_stack = []

    def close_lists(current_indent=0):
        while list_stack and list_stack[-1] >= current_indent:
            html.append("</ul>\n")
            list_stack.pop()

    for line in lines:
        line_stripped = line.rstrip()
        if not line_stripped:
            close_lists(0)
            continue

        # Headings
        if re.match(r"^(#{1,6})\s+", line_stripped):
            close_lists(0)
            m = re.match(r"^(#{1,6})\s+(.*)", line_stripped)
            level, text = len(m.group(1)), m.group(2)
            html.append(f"<h{level}>{text}</h{level}>\n")
            continue

        # List items
        m = re.match(r"^(\s*)([-*+])\s+(.*)", line)
        if m:
            indent = len(m.group(1))
            text = m.group(3)

            if not list_stack or indent > list_stack[-1]:
                html.append("<ul>\n")
                list_stack.append(indent)
            elif indent < list_stack[-1]:
                close_lists(indent)

            text = re.sub(r"\*\*(.*?)\*\*", r"<strong>\1</strong>", text)
            text = re.sub(r"\*(.*?)\*", r"<em>\1</em>", text)
            text = re.sub(r"`(.*?)`", r"<code>\1</code>", text)
            text = re.sub(r"\[(.*?)\]\((.*?)\)", r'<a href="\2">\1</a>', text)

            html.append(f"<li>{text}</li>\n")
            continue

        # Not a list, close any open lists
        close_lists(0)

        # Inline formatting for paragraphs
        text = re.sub(r"\*\*(.*?)\*\*", r"<strong>\1</strong>", line_stripped)
        text = re.sub(r"\*(.*?)\*", r"<em>\1</em>", text)
        text = re.sub(r"`(.*?)`", r"<code>\1</code>", text)
        text = re.sub(r"\[(.*?)\]\((.*?)\)", r'<a href="\2">\1</a>', text)

        html.append(f"<p>{text}</p>\n")

    close_lists(0)
    return "".join(html)
