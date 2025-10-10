from setuptools import setup, find_packages

setup(
    name="InstaHanz",
    version="1.0.0",
    description="Instagram OSINT Tool - Profil analizi, gönderi takibi, AI tabanlı bot tahmini",
    author="Mahmut Balıkçı",
    packages=find_packages(),
    install_requires=[
        "instaloader>=4.14.2",
        "requests>=2.32.0",
        "click>=8.3.0",
        "python-dotenv>=1.1.1",
        "textblob>=0.17.1"
    ],
    entry_points={
        "console_scripts": [
            "InstaHanz=InstaHanz.__main__:main",
        ],
    },
    python_requires=">=3.10",
)
