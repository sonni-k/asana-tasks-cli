from setuptools import setup, find_packages

setup(
    name="asana_tasks",
    version="0.1",
    py_modules=["main"],
    install_requires=["asana"],
    entry_points={
        "console_scripts": [
            "asana=main:main",
        ],
    },
)
