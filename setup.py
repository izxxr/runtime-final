from setuptools import setup

with open("README.MD", "r", encoding="utf-8") as f:
    LONG_DESCRIPTION = f.read()

VERSION = "1.0.0"
GITHUB = "https://github.com/nerdguyahmad/runtime-final"
DOCUMENTATION = "https://github.com/nerdguyahmad/runtime-final/wiki"
LICENSE = "MIT"
PACKAGES = ["runtime_final"]


setup(
    name="runtime-final",
    author="nerdguyahmad",
    version=VERSION,
    license=LICENSE,
    url=GITHUB,
    project_urls={
        "Documentation": DOCUMENTATION,
        "Issue tracker": GITHUB + "/issues",
    },
    description='Declare final Python classes and methods at runtime.',
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    include_package_data=True,
    packages=PACKAGES,
    python_requires='>=3.6.0',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved :: MIT License',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Topic :: Internet',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Utilities',
        'Typing :: Typed',
    ]
)
