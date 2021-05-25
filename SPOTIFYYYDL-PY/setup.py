from setuptools import setup, find_packages
from spotifyyy_dl.printf import VERSION
setup(
    name='spotifyyy-dl',
    version=VERSION,
    license="Apache2",
    description="Spotify Music Downloader.",

    author='YaronH',
    author_email="yaronhuang@foxmail.com",

    packages=find_packages(),
    include_package_data=True,
    platforms="any",
    install_requires=["aigpy>=2021.3.25.2", 
                      "requests>=2.22.0", 
                      "pycryptodome", 
                      "pydub", 
                      "prettytable",
                      "spotipy",
                      "ytmusicapi",
                      "pytube"],
    entry_points={'console_scripts': ['spotifyyy-dl = spotifyyy_dl:main', ]}
)
