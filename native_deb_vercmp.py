import apt
import apt_pkg
import sys


if len(sys.argv) < 3:
    raise StandardError("Need two versions to compare!")

ver1 = sys.argv[1]
ver2 = sys.argv[2]

vc = apt_pkg.version_compare(ver1, ver2)

if vc > 0:
    sys.stdout.write("%s > %s\n" % (ver1,ver2))
elif vc == 0:
    sys.stdout.write("%s = %s\n" % (ver1,ver2))
elif vc < 0:
    sys.stdout.write("%s < %s\n" % (ver1,ver2))
