from setuptools import setup

setup(
    name="pm",
    version="1.0.0",
    description="cli password manager",
    python_requires=">=3.10",
    package_dir={"": "src"},
    py_modules=["entry", "main", "utils", "vault"],
    install_requires=[
        "argon2-cffi",
        "cryptography",
    ],
    entry_points={
        "console_scripts": [
            "pm=main:main",
        ],
    },
)
