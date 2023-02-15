import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="indxr",
    version="0.1.2",
    author="Elias Bassani",
    author_email="elias.bssn@gmail.com",
    description="indxr: A Python utility for indexing long files.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/AmenRa/indxr",
    packages=setuptools.find_packages(),
    install_requires=[
        "numpy",
        "orjson",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Intended Audience :: Science/Research",
        "Operating System :: OS Independent",
        "Topic :: Text Processing :: General",
    ],
    keywords=[
        "text index",
        "file index",
        "index",
        "indexer",
        "indexing",
        "information retrieval",
        "natural language processing",
    ],
    python_requires=">=3.7",
)
