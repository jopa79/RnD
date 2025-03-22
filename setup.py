from setuptools import setup, find_packages
import os

# Get the version from the package
about = {}
with open(os.path.join("image_harvester", "__init__.py"), "r", encoding="utf-8") as f:
    exec(f.read(), about)

# Read the README for the long description
with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="image_harvester",
    version=about["__version__"],
    author="",
    author_email="",
    description="A desktop application for downloading and processing images from Bing",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jopa79/RnD",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=[
        "customtkinter>=5.2.0",
        "pillow>=9.5.0",
        "requests>=2.30.0",
        "python-dotenv>=1.0.0",
        "tqdm>=4.65.0",
    ],
    entry_points={
        "console_scripts": [
            "image_harvester=image_harvester.main:main",
        ],
    },
)
