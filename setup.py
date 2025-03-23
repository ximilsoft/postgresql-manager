from setuptools import setup, find_packages

setup(
    name="postgresql_manager",
    version="2.0.0",
    author="Xandor Telvanyx",
    author_email="xandortelvanyx@ximilsoft.com",
    description="A simple PostgreSQL management package for handling databases, tables, columns, and rows.",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/ximilsoft/postgresql_manager",
    packages=find_packages(),
    install_requires=[
        "psycopg2",
    ],
    classifiers=[  # Optional but recommended
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",  # Ensures Python version compatibility
)
