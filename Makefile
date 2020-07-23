
default:
	@ echo "Invalid usage.\nmake [test/publish]"

test:
	@ tox

publish:
	@ rm -rf dist/
	@ python3 setup.py sdist bdist_wheel
	@ python3 -m twine upload --repository pypi dist/*
