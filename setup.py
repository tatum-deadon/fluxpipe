from setuptools import setup, find_packages

setup(
    name="fluxpipe",
    version="0.1.0",
    author="Tatum Deadon",
    description="Lightweight CI/CD pipeline engine",
    packages=find_packages(),
    python_requires=">=3.9",
    extras_require={"dev": ["pytest>=7.0", "pyyaml"]},
    install_requires=["pyyaml>=6.0"],
    entry_points={"console_scripts": ["fluxpipe=fluxpipe.__main__:main"]},
)
