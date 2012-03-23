#!/usr/bin/python2

from HTMLParser import HTMLParser, HTMLParseError
from urllib2 import urlopen, HTTPError
from os import path, makedirs
from sys import argv, exit

class MyHtmlParser(HTMLParser):
    capture = False

    def set_destination(self, destination):
        self.destination = destination

    def handle_starttag(self, tag, attrs):
        if tag == "td":
            if len(attrs) == 1 and attrs[0] == ("class", "mulink"):
                self.capture = True
        elif self.capture == True and tag == "a":
            if len(attrs) == 2 and attrs[1] == ("title", "Click to Play"):
                url = attrs[0][1]
                url = url.split("'")[1].strip()

                basename = url[url.rfind("/") + 1:].replace(" ", "_")
                directory = path.join(self.destination, basename[0])
                if not path.exists(directory):
                    makedirs(directory)
                pathname = path.join(directory, basename)

                url = url.replace(" ", "%20")

                print "< %s" % url
                print "> %s" % pathname
                outfile = open(pathname, "wb")
                infile = urlopen(url)
                outfile.write(infile.read())
                outfile.close()

    def handle_endtag(self, tag):
        if tag == "td":
            self.capture = False

if __name__ == "__main__":
    if len(argv) != 2:
        print "Usage: ./rip.py destination"
        exit(1)

    start = 0
    end = 6600
    step = 50
    base_url = "http://www.recordedamigagames.org/modules/music/index.php?min="

    for i in range(start, end + step, step):
        print
        print "Index: %d" % i
        print "-" * 80
        doc = urlopen("%s%d" % (base_url, i))

        parser = MyHtmlParser()
        parser.set_destination(argv[1])
        try:
            parser.feed(doc.read())
        except HTMLParseError:
            pass
        except HTTPError as e:
            print e
