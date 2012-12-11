try:
    from setuptools import setup
except ImportError:
    from distutils import setup


def load_readme():
    readme_file = "README"
    try:
        return open(readme_file, 'r').read()
    except Exception:
        raise RuntimeError("Cannot find readme file {fname}.".format(
            fname=readme_file))


def load_version():
    """Open and parse out the version number from the _version.py module.

    Because of namespacing wtftz.wtfz.converter.convert to wtftz.convert,
    which has the dependencies listed below, I can't import __version__ from
    __init__.py. Open and parse wtftz/_version.py instead.

    Inspired by http://stackoverflow.com/a/7071358
    """
    import re
    version_file = "wtftz/_version.py"
    version_line = open(version_file).read().rstrip()
    vre = re.compile(r'__version__ = "([^"]+)"')
    matches = vre.findall(version_line)
    if matches and len(matches) > 0:
        return matches[0]
    else:
        raise RuntimeError(
            "Cannot find version string in {version_file}.".format(
                version_file=version_file))

version = load_version()
long_description = load_readme()

setup(
    name='wtftz',
    version=version,
    description="Convert a timestamp from one timezone to another",
    long_description=long_description,
    author='Steven Buss',
    author_email='steven.buss@gmail.com',
    url='https://github.com/sbuss/wtftz',
    download_url=('https://github.com/sbuss/wtftz/tarball/v%s' % version),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 2.7",
    ],
    packages=[
        'wtftz',
    ],
    scripts=[
        'bin/wtftz',
    ],
    install_requires=[
        'python-dateutil>=1.5',
        'pytz',
    ],
)
