from setuptools import setup

setup(
    name="socket_video_stream",
    version="0.0.0",
    author="Andrew Golovashevich",
    packages=["socket_video_stream"],
    package_dir={"socket_video_stream": "src"},
    package_data={"socket_video_stream": ["py.typed", "__init__.pyi"]},
    classifiers=[
        "Development Status :: 4 - Beta",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Multimedia :: Graphics :: Capture :: Digital Camera",
        "Topic :: Multimedia :: Video :: Display",
        "Topic :: Software Development :: Version Control :: Git",
        "Typing :: Typed"
    ],
    url="https://github.com/LandgrafHomyak/SocketVideoStream",
    entry_points={
        "console_scripts": [
            "svs_client = socket_video_stream._client:main",
            "svs_server = socket_video_stream._server:main"

        ]
    }
)
