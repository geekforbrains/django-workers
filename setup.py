import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="django-workers",
    version="0.1.3",
    author="Gavin Vickery",
    author_email="gavin@geekforbrains.com",
    description="Simple background tasks for Django",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/geekforbrains/django-workers",
    packages=setuptools.find_packages(),
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
)
