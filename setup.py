from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="supers",
    version="0.2.0",
    author="Lukas Hedegaard",
    description="Call a function in all superclasses as easy as `supers(self).foo(42)`",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/LukasHedegaard/supers",
    python_requires=">=3.6",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta",
        "Framework :: Pytest",
        "Topic :: Utilities",
    ],
    packages=find_packages(),
    install_requires=[],
    extras_require={
        "tests": ["pytest", "pytest-cov", "flake8", "flake8-black",],
        "build": ["setuptools", "wheel", "twine"],
    },
)
