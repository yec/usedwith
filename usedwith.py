#!/usr/bin/env python
"""
 Used with
 Find the part and used with part
 Takes one filename as argument:

    python usedwith.py data.xml

 To write to file and only keep uniq rows:

    python usedwith.py data.xml | uniq > output.txt

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
    partpattern = re.compile('PNR.+?PID="(.+?)".*?>(.+?)</PNR', re.S)
    usedpattern = re.compile('UWP.+?PID="(.+?)".*?>(.+?)</UWP', re.S)
    einpattern = re.compile('EIN.+?TYPE="(.+?)".*?>(.+?)</EIN', re.S)
    revdatepattern = re.compile('REVDATE="(.+?)"', re.S)
    keypattern = re.compile('KEY="(.+?)"', re.S)

    print "Key\tRevision Date\tPNR PID\tPart Number\tUWP PID\tUsed With Part Number\tEIN\tEIN Type"

    for match in matches:

        """ submatch part number """
        key = keypattern.search(match).group(1).strip()
        revdate = revdatepattern.search(match).group(1).strip()
        part_pid =  partpattern.search(match).group(1).strip()
        part =  partpattern.search(match).group(2).strip()

        iters = 0;
        for m in re.finditer('<UWPMFR', match, re.S):
            iters = iters + 1
            start = m.start()
            used_with_pid = usedpattern.search(match[start:]).group(1).strip()
            used_with = usedpattern.search(match[start:]).group(2).strip()
            print "%s\t%s\t%s\t%s\t%s\t%s" % (key, revdate, part_pid, part, used_with_pid, used_with)

        for m in re.finditer('<EIN', match, re.S):
            iters = iters + 1
            start = m.start()
            ein = einpattern.search(match[start:]).group(2).strip()
            ein_type = einpattern.search(match[start:]).group(1).strip()
            print "%s\t%s\t%s\t%s\t\t\t%s\t%s" % (key, revdate, part_pid, part, ein, ein_type)

        """ print out part number without used with if not found """
        if iters == 0:
            print "%s\t%s\t%s\t%s" % (key, revdate, part_pid, part)


if __name__ == "__main__":
    main()

