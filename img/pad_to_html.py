import sys
import bleach
from markdown2 import markdown

from urllib2 import urlopen


def main():
    source, destination = sys.argv[1:]

    source = urlopen(source + "/export/txt").read()
    source = "\n".join(filter(lambda x: not x.lstrip().startswith("//"), source.split("\n")))
    html = markdown(source)

    open(destination, "w").write(html)


if __name__ == '__main__':
    main()
