from setuptools import setup, find_packages
import os

if os.path.exists('README.md'):
    with open("README.md", "r", encoding="utf-8") as fh:
        long_description = fh.read()
else:
    long_description = 'An async bloom filter library for Python.'

setup(
    name="aiobloom_live",
    version="0.1.1",
    author="ASXE",
    author_email="2973918177@qq.com",
    description="An async bloom filter library for Python.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/asxez/aiobloom_live",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Utilities",
    ],
    python_requires='>=3.7',
    install_requires=[
        "bitarray>=0.3.4",
        "aiofiles",
        "xxhash"
    ],
)
