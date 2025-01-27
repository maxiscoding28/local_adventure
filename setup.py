from setuptools import setup, find_packages

setup(
    name="local_adventure",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "click",  # Ensure click is installed
    ],
    entry_points={
        "console_scripts": [
            "locadv=local_adventure.cli:locadv",  # Maps 'locadv' to the 'la' function in cli.py
        ],
    },
    author="Your Name",
    description="A CLI for Local Adventure.",
    long_description="A command-line tool to start your local adventures!",
    long_description_content_type="text/markdown",
    url="https://your-repo-link.com",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)