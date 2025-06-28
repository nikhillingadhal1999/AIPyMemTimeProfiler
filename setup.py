from setuptools import setup, find_packages

setup(
    name="aipymemtimeprofiler",
    version="1.0.8",
    author="Nikhil Lingadhal",
    description="AI-enabled time and memory profiler for Python applications",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/nikhillingadhal1999/AIPyMemTimeProfiler",
    license="MIT",
    packages=find_packages(),  # auto-detects submodules in aipymemtimeprofiler/
    install_requires=[
        "line_profiler==4.2.0",
        "psutil==7.0.0",
        "Pympler==1.1",
        "rich",
        "Flask",
        "memory_profiler",
        "setuptools",
        "wheel",
        "twine",
        "ollama",
        "packaging>=23.2,<25",
        "streamlit",
        "plotly",
        "pandas"
    ],
    entry_points={
        "console_scripts": [
            "profile_code = aipymemtimeprofiler.executable.execute:run_with_profiler",
            "profile_graph = aipymemtimeprofiler.vizualization.viz:main"
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)
