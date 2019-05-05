import setuptools

setuptools.setup(
    # FIXME(), if not add package_data and include_package_data
    # some files which ends with .ini or other will be missed
    package_data={
        # If any package contains *.ini or *.txt files, include them:
        '': ['*.ini', '*.mako', '*.yaml', '*.txt', '*.py', 'README', '*.json', '*.wsgi'],
    },
    include_package_data=True,
    setup_requires=['pbr'],
    pbr=True)