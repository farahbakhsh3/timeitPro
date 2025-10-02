from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="timeitPro",
    version="0.1.0",
    author="ّFarahbakhsh3",
    author_email="farahbakhsh3@gmail.com",
    description="Advanced Python function profiler with JSON logging and Flask dashboard",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/farahbakhsh3/timeitPro",
    packages=find_packages(),
    python_requires=">=3.7",
    install_requires=[
        "Flask>=2.0.0",
        "psutil>=5.9.0"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU License",
        "Operating System :: OS Independent",
    ],
    entry_points={
        "console_scripts": [
            "timeitPro-dashboard=timeitPro.dashboard:run_dashboard",
        ],
    },
)
