import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="cqi",
    version="1.0.0",
    author="Patrick Jentsch",
    author_email="patrickjentsch@gmx.net",
    description=('A Python library for the IMS Open Corpus Workbench (CWB) '
                 'corpus query interface (CQi) API.'),
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Pevtrick/cqi-py",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.5',
)
