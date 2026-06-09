from setuptools import setup, find_packages

setup(
    name="sonicweave",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "psutil",
        "rich",
        "google-genai",
        "requests",
        "python-dotenv",
    ],
    entry_points={
        "console_scripts": [
            "sonicweave=sonicweave.main:main",
        ],
    },
    author="Pkkarthik12",
    description="AI-powered music curator and USB/SD burner.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/Pkkarthik12/SonicWeave",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.9',
)
