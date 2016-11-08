#!/bin/sh
case $1 in
	install)
		echo "install"
		python setup.py install
		;;
	uninstall)
		echo "uninstall"
		pip uninstall crecomp -y
		;;
	publish)
		echo "readme"
		pandoc -o README.rst README.md
		;;
	release)
		echo "release"
		pandoc -o README.rst README.md
		# python crecomp/scrp_yacc.py
		python setup.py egg_info sdist bdist_wheel
		python setup.py register
		python setup.py sdist upload
		rm -rf dist
		rm -rf crecomp.egg-info
		rm -rf build
		;;
	clean)
		echo "cleaned files"
		rm crecomp/*pyc
		rm -rf dist
		rm -rf crecomp.egg-info
		rm -rf build
		;;
	*)
		echo "option list"
		echo "=========="
		echo "install"
		echo "uninstall"
		echo "publish"
		echo "release"
		echo "clean"
		;;
esac