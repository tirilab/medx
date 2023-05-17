
from setuptools import setup, find_packages
import pathlib

here = pathlib.Path(__file__).parent.resolve()

# Get the long description from the README file
long_description = (here / "README.md").read_text(encoding="utf-8")

setup(
    name="medx",  
    version="0.1", 
    description="A python package to automate the calculation of Medication Regimen Complexity from EHR data.",  
    long_description=long_description,  
    long_description_content_type="text/markdown",  
    url="https://github.com/pypa/sampleproject",  
    author="Louise Lu", 
    author_email="ylu106@jhu.edu", 
    # Classifiers help users find your project by categorizing it.
    #
    # For a list of valid classifiers, see https://pypi.org/classifiers/
    classifiers=[  # Optional
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Clinical Researcher",
        "Topic :: Software Development :: Build Tools",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
    ],
    # You can just specify package directories manually here if your project is
    # simple. Or you can use find_packages().
    #
    # Alternatively, if you just want to distribute a single Python file, use
    # the `py_modules` argument instead as follows, which will expect a file
    # called `my_module.py` to exist:
    #
    #   py_modules=["my_module"],
    #
    packages=find_packages(),  # Required
    python_requires=">=3.7, <4",
    # This field lists other packages that your project depends on to run.
    # Any package you put here will be installed by pip when your project is
    # installed, so they must be valid existing projects.
    #
    # For an analysis of "install_requires" vs pip's requirements files see:
    # https://packaging.python.org/discussions/install-requires-vs-requirements/
    install_requires=["numpy", "pandas"],  
    package_data={ 
        "ndc": ["data/ndc_database.xlsx"],
        "keywordA":["data/keywordsA.csv"],
        "keywordB":["data/keywordsB.csv"],
        "keywordC":["data/keywordsC.csv"],
    },
)