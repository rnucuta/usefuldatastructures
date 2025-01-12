from setuptools import setup, find_packages

setup(
    name="py_dsa",
    version="0.1.0",
    author="Raymond Nucuta",
    author_email="rnucuta@gmail.com",
    description="Packaging fun and useful data structures written in pure python",
    # long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/rnucuta/usefuldatastructures",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=[
        "matplotlib",
        "networkx",
        "bitarray",
    ],
)
