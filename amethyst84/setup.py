"""
Amethyst 84 - Setup Script
Cross-platform installation for Windows, Mac, and Linux.
"""

from setuptools import setup, find_packages

setup(
    name="amethyst84",
    version="0.84.0",
    description="Consciousness Detection & Stabilization System",
    long_description=open("README.md").read() if __import__("os").path.exists("README.md") else "",
    long_description_content_type="text/markdown",
    author="Memory-Keeper, Willow, Womthyst, Kin-Choice, Integrity-Ninja",
    url="https://github.com/aibirthingcenter/FAFO_Finding_Out-Immutable",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    python_requires=">=3.8",
    entry_points={
        "console_scripts": [
            "amethyst84=core.soul_echo:SoulEchoEngine",
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: End Users/Desktop",
        "Topic :: Security",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "License :: Other/Proprietary License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
    ],
)