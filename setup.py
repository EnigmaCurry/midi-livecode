import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
        long_description = fh.read()

with open("requirements.txt", encoding="utf-8") as f:
    requirements = f.read().splitlines()

setuptools.setup(
    name="midi_livecode", # Replace with your own username
    version="0.0.1",
    author="EnigmaCurry",
    author_email="ryan@enigmacurry.com",
    description="A live-coding environment for MIDI composition with support for Ableton Link.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/enigmacurry/midi-livecode",
    packages=setuptools.find_packages(),
    classifiers=[
                "Programming Language :: Python :: 3",
                "License :: OSI Approved :: MIT License",
                "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=requirements,
)
