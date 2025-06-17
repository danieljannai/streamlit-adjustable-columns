from setuptools import setup, find_packages
import os

# Read the README file
this_directory = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(this_directory, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="streamlit-expandable-columns",
    version="0.1.0",
    author="Daniel Jannai Epstein",
    description="A Streamlit custom component for creating columns with adjustable widths",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/danieljannai/streamlit-expandable-columns",
    packages=find_packages(),
    include_package_data=True,
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Framework :: Streamlit",
    ],
    python_requires=">=3.7",
    install_requires=[
        "streamlit>=0.63",
    ],
) 