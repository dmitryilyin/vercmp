#!/bin/sh
ver1="${1}"
ver2="${2}"

if [ -z "${ver1}" -o -z "${ver2}" ]; then
  echo "Give two versions to compare!"
  exit 1
fi

dir=$(dirname ${0})
cd "${dir}" || exit 1

echo "* Native Puppet"
ruby native_puppet_vercmp.rb "${ver1}" "${ver2}"

echo "* Puppet RPMVERCMP"
ruby rpm_puppet_vercmp.rb "${ver1}" "${ver2}"

echo "* Native RPM"
python native_rmp_vercmp.py "${ver1}" "${ver2}"

echo "* Native DEB"
python native_deb_vercmp.py "${ver1}" "${ver2}"