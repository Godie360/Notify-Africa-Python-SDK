from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="notify-africa",
    version="1.0.0",
    author="Godfrey Enosh",
    author_email="godfreyenos360@gmail.com",
    description="Python SDK for Notify Africa API",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/Godie360/Notify-Africa-Python-SDK",
    packages=find_packages(),
    install_requires=[
        "requests>=2.25.0",
        "pandas>=1.3.0",
        "openpyxl>=3.0.7",
        "python-dateutil>=2.8.0",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)