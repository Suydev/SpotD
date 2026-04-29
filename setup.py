from setuptools import setup, find_packages

setup(
    name="spotdl",
    version="1.0.0",
    author="SpotDL Team",
    description="Spotify Downloader",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/Suydev/SpotD",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    python_requires=">=3.10",
    install_requires=[
        "flask",
        "flask-sqlalchemy",
        "spotipy",
        "qrcode",
        "yt-dlp",
        "python-dotenv",
        "mutagen",
        "tqdm",
        "colorama",
        "psutil",
        "pillow",
        "requests",
        "gunicorn",
    ],
    entry_points={
        "console_scripts": [
            "spotdl=spotdl.cli:main",
        ],
    },
)