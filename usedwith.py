#!/usr/bin/env python
"""
 Used with
 Find the part and used with part

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

    matches = re.findall('<ITEM.+?UWPMFR.+?</ITEM', data, re.S)

    """ Folowing pattern extracts part number and used with part number with submatches"""
    pattern = re.compile('PNR [^>]+>(.+?)</PNR.+?UWP [^>]+>(.+?)</UWP', re.S)

    print "Part Number\tUsed With Part Number"

    for match in matches:
        part =  pattern.search(match).group(1).strip()
        used_with = pattern.search(match).group(2).strip()
        print "%s\t%s" % (part, used_with)


if __name__ == "__main__":
    main()

