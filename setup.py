import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="sqlar",
    version="1.0.1",
    author="Pavel V. Pristupa",
    author_email="pristupa@gmail.com",
    description="SQLAlchemy implementation for Python Persistance API (persipy)",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pristupa/sqlar",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        'injector==0.15.0',
        'persipy==2.0.0',
        'sqlalchemy==1.3.0',
    ],
)
