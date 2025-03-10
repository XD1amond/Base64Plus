from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="base64plus",
    version="0.1.0",
    author="Base64Plus Team",
    author_email="info@base64plus.example.com",
    description="Transform images into AI-ready data with embedded text and positions",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/base64plus",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=[
        "Pillow>=8.0.0",
        # Optional dependencies are handled in the code
    ],
    extras_require={
        "easyocr": ["easyocr>=1.4.1"],
        "tesseract": ["pytesseract>=0.3.8"],
        "all": ["easyocr>=1.4.1", "pytesseract>=0.3.8"],
    },
)