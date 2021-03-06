#!/usr/bin/python
#
# rpmdev-vercmp -- compare rpm versions
#
# Copyright (c) Seth Vidal
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA

import rpm
import sys

def stringToVersion(verstring):
    if verstring in [None, '']:
        return (None, None, None)
    i = verstring.find(':')
    if i != -1:
        try:
            epoch = str(long(verstring[:i]))
        except ValueError:
            # look, garbage in the epoch field, how fun, kill it
            epoch = '0' # this is our fallback, deal
    else:
        epoch = '0'
    j = verstring.find('-')
    if j != -1:
        if verstring[i + 1:j] == '':
            version = None
        else:
            version = verstring[i + 1:j]
        release = verstring[j + 1:]
    else:
        if verstring[i + 1:] == '':
            version = None
        else:
            version = verstring[i + 1:]
        release = None
    return (epoch, version, release)

def usage():
    print """
rpmdev-vercmp <epoch1> <ver1> <release1> <epoch2> <ver2> <release2>
rpmdev-vercmp <EVR1> <EVR2> # if rpmUtils.miscutils is available
rpmdev-vercmp # with no arguments, prompt

Exit status is 0 if the EVR's are equal, 11 if EVR1 is newer, and 12 if EVR2
is newer.  Other exit statuses indicate problems.
"""

def vercmp((e1, v1, r1), (e2, v2, r2)):
   rc = rpm.labelCompare((e1, v1, r1), (e2, v2, r2))
   return rc


def askforstuff(thingname):
    thing = raw_input('%s :' % thingname)
    return thing

def main():
    if len(sys.argv) > 1 and sys.argv[1] in ['-h', '--help', '-help', '--usage']:
        usage()
        sys.exit(0)
    elif len(sys.argv) == 3:
        (e1, v1, r1) = stringToVersion(sys.argv[1])
        (e2, v2, r2) = stringToVersion(sys.argv[2])
        # stringToVersion in yum < 3.1.2 may return numeric (non-string)
        # Epochs, and labelCompare does not like that.
        if e1 is not None: e1 = str(e1)
        if e2 is not None: e2 = str(e2)
    elif len(sys.argv) < 7:
        e1 = askforstuff('Epoch1')
        v1 = askforstuff('Version1')
        r1 = askforstuff('Release1')        
        e2 = askforstuff('Epoch2')
        v2 = askforstuff('Version2')
        r2 = askforstuff('Release2')
    else:
        (e1, v1, r1, e2, v2, r2) = sys.argv[1:]
   
    rc = vercmp((e1, v1, r1), (e2, v2, r2))
    if rc > 0:
        print "%s:%s-%s > %s:%s-%s" % (e1, v1, r1, e2, v2, r2)
        rc = 11
    elif rc == 0:
        print "%s:%s-%s = %s:%s-%s" % (e1, v1, r1, e2, v2, r2)
    elif rc < 0:
        print "%s:%s-%s < %s:%s-%s" % (e1, v1, r1, e2, v2, r2)
        rc = 12
    sys.exit(rc)

if __name__ == "__main__":
    main()
