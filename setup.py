try:
    from setuptools import setup
except ImportError:
    from distutils import setup

from wtftz import __version__

setup(
    name='wtftz',
    version=__version__,
    description="Convert a timestamp from one timezone to another",
    long_description=open("README.md").read(),
    author='Steven Buss',
    author_email='steven.buss@gmail.com',
    url='https://github.com/sbuss/wtftz',
    download_url=('https://github.com/sbuss/wtftz/tarball/v%s' % __version__),
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
        'scripts/wtftz',
    ],
    install_requires=[
        'python-dateutil>=1.5',
        'pytz',
    ],
)
