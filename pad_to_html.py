import sys
import bleach
from markdown2 import markdown

from urllib2 import urlopen


# built from here https://www.w3.org/TR/html-markup/elements.html
ALLOWED_TAGS = (
    "a",
    "abbr",
    "b",
    "blockquote",
    "br",
    "col",
    "colgroup",
    "dd",
    "del",
    "div",
    "dl",
    "dt",
    "em",
    "footer",
    "h1",
    "h2",
    "h3",
    "h4",
    "h5",
    "h6",
    "head",
    "header",
    "hgroup",
    "hr",
    "i",
    "img",
    "label",
    "legend",
    "li",
    "nav",
    "ol",
    "p",
    "pre",
    "q",
    "s",
    "section",
    "small",
    "span",
    "strong",
    "table",
    "tbody",
    "td",
    "tfoot",
    "th",
    "thead",
    "time",
    "title",
    "tr",
    "u",
    "ul",
    "wbr",
)

header = """
<!doctype html>
<html>
<head>
<title>Neutrinet Hub</title>
<link href="../css/pad.css" rel="stylesheet">
<body>
"""

footer = """
</body>
</html>
"""

def main():
    source, destination = sys.argv[1:]

    source = urlopen(source + "/export/txt").read()
    source = "\n".join(filter(lambda x: not x.lstrip().startswith("//"), source.split("\n")))
    html = bleach.clean(markdown(source), tags=ALLOWED_TAGS)

    html = header + html + footer

    open(destination, "w").write(html)


if __name__ == '__main__':
    main()
