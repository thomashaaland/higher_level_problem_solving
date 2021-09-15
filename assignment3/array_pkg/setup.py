import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()


setuptools.setup(
        name="array_package",
        version="0.1",
        author="Thomas Haaland",
        author_email="thomhaa@ifi.uio.no",
        description="This is a custom implementation of arrays",
        packages=setuptools.find_packages(),
        )
