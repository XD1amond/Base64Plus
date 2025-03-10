"""
Base64Plus - Transform images into AI-ready data with embedded text and positions.

This library processes images by extracting text and positional metadata,
then encodes both the image and extracted metadata into an AI-ready Base64+ format.
"""

from .base64plus import encode_base64plus, decode_base64plus

__version__ = '0.1.0'
__all__ = ['encode_base64plus', 'decode_base64plus']