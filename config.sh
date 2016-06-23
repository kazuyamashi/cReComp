#!/bin/sh
case $1 in
	install)
		echo "install"
		python setup.py install
		;;
	uninstall)
		echo "uninstall"
		pip uninstall crecomp -y
		rm -rf dist
		rm -rf crecomp.egg-info
		rm -rf build
		;;
	release)
		echo "release"
		python setup.py egg_info sdist bdist_wheel
		python setup.py register
		python setup.py sdist upload
		rm -rf dist
		rm -rf crecomp.egg-info
		rm -rf build
		;;
	clean)
		echo "cleaned files"
		rm -rf dist
		rm -rf crecomp.egg-info
		rm -rf build
		;;
	*)
		echo "argument error"
		;;
esac