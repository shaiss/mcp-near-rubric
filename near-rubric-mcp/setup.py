from setuptools import setup, find_packages

setup(
    name="near-rubric-mcp",
    version="0.1.0",
    description="MCP Server for NEAR Protocol project evaluation",
    author="NEAR Development Program",
    packages=find_packages(),
    install_requires=[
        "pyyaml>=6.0",
        "asyncio>=3.4.3",
    ],
    python_requires=">=3.7",
    include_package_data=True,
    package_data={
        "": ["resources/prompts/*.txt", "config/*.yaml"],
    },
    entry_points={
        "console_scripts": [
            "near-rubric-mcp=near-rubric-mcp.server:main",
        ],
    },
) 