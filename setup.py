from setuptools import setup, find_packages
import requests
import os


# 将markdown格式转换为rst格式
def md_to_rst(from_file, to_file):
    r = requests.post(url='http://c.docverter.com/convert',
                      data={'to': 'rst', 'from': 'markdown'},
                      files={'input_files[]': open(from_file, 'rb')})
    if r.ok:
        with open(to_file, "wb") as f:
            f.write(r.content)

md_to_rst("README.md", "README.rst")

if os.path.exists('README.rst'):
    with open("README.rst", "r", encoding="utf-8") as fh:
        long_description = fh.read()
else:
    long_description = 'An async bloom filter library for Python.'



setup(
    name="aiobloom_live",
    version="0.1.0",
    author="ASXE",
    author_email="2973918177@qq.com",
    description="An async bloom filter library for Python.",
    long_description=long_description,
    long_description_content_type="text/x-rst",
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
        "Topic :: Utilities",
    ],
    python_requires='>=3.7',
    install_requires=[
        "bitarray>=0.3.4",
        "aiofiles",
        "xxhash"
    ],
)
