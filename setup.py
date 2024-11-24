from setuptools import setup, find_packages

setup(
    name="dbt-break-detector",
    version="0.1.0",
    package_dir={"": "src"},  # Tell setuptools packages are under src
    packages=find_packages(where="src"),
    install_requires=[
        "dbt-core>=1.5.0",
        "networkx>=2.8.0",
        "pyyaml>=6.0",
        "gitpython>=3.1.0",
        "click>=8.0.0"
    ],
    entry_points={
        "console_scripts": [
            "dbt-break-detector=src.cli:main",
        ],
    },
    author="Your Name",
    author_email="your.email@example.com",
    description="A tool to detect breaking changes in dbt projects",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/dbt-break-detector",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
)