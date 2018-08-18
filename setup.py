import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="app-settings",
    version="1.0.0",
    author="Ugur UKER [Arcticle Intelligence Labs]",
    author_email="uguruker@gmail.com",
    description="An interface providing you the ability to easily manage application context settings",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/arcticle/app-settings.git",
    packages=setuptools.find_packages(exclude=["tests"]),
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
)