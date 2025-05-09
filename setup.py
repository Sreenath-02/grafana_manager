from setuptools import setup, find_packages

setup(
    name="grafana-manager",
    version="1.0.0",
    description="A Python library for managing Grafana datasources, dashboards, and panels.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Sreenath",
    author_email="msreenathreddy2001@gmail.com",
    url="https://github.com/yourusername/grafana-manager",  # Replace with your repo URL
    packages=find_packages(),
    install_requires=[
        "requests"  # Add any dependencies here
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)