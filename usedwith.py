#!/usr/bin/env python
"""
 Used with
 Find the part and used with part
 Takes one filename as argument

    python usedwith.py data.xml

 @author    Ye Chuah
 @copyright invenn.com.au
 @created   24/03/2012
 @license   GPL

"""

import re
import sys

def main():
    if (len(sys.argv) > 1):
        filename = sys.argv[1]
    else:
        filename = 'data.xml'

    try:
        f = open(filename, 'r')
        data = f.read()
        f.close()
        print "Using %s" % filename
    except Exception:
        print "Couldn't open %s" % filename
        sys.exit(0)

    matches = re.findall('<ITEM.+?</ITEM', data, re.S)

    """ Folowing pattern extracts part number and used with part number with submatches"""
    partpattern = re.compile('PNR [^>]+>(.+?)</PNR', re.S)
    usedpattern = re.compile('UWP [^>]+>(.+?)</UWP', re.S)

    print "Part Number\tUsed With Part Number"

    for match in matches:

        """ submatch part number """
        part =  partpattern.search(match).group(1).strip()

        iters = 0;
        for m in re.finditer('<UWPMFR', match, re.S):
            iters = iters + 1
            start = m.start()
            used_with = usedpattern.search(match[start:]).group(1).strip()
            print "%s\t%s" % (part, used_with)

        """ print out part number without used with if not found """
        if iters == 0:
            print "%s" % part


if __name__ == "__main__":
    main()

