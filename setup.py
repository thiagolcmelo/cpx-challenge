from setuptools import setup, find_packages

with open("README.md", "r") as f:
    readme = f.read()

with open("requirements.txt", "r") as f:
    dependencies = [l.replace("\n", "") for l in f.readlines()]

setup(
    name="CPX Utils CLI",
    version="0.0.1",
    author="Thiago Melo",
    author_email="thiago.lc.melo@gmail.com",
    description=(
        "CLI tool for fetching information about servers and services from CPX API."
    ),
    license="BSD",
    keywords="cli cpx utils",
    packages=find_packages(),
    long_description=readme,
    include_package_data=True,
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities",
        "License :: OSI Approved :: BSD License",
    ],
    entry_points={
        "console_scripts": [
            "cpx_utils=src.cli:main",
        ]
    },
    install_requires=dependencies,
    python_requires=">=3.8",
)
