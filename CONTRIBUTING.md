# Contributing to Base64Plus

Thank you for your interest in contributing to Base64Plus! This document provides guidelines and instructions for contributing to this project.

## Code of Conduct

Please be respectful and considerate of others when contributing to this project. We aim to foster an inclusive and welcoming community.

## How to Contribute

### Reporting Bugs

If you find a bug, please create an issue with the following information:

- A clear, descriptive title
- A detailed description of the issue
- Steps to reproduce the bug
- Expected behavior
- Actual behavior
- Screenshots (if applicable)
- Environment information (OS, language version, etc.)

### Suggesting Enhancements

We welcome suggestions for enhancements! Please create an issue with:

- A clear, descriptive title
- A detailed description of the proposed enhancement
- Any relevant examples or use cases

### Pull Requests

1. Fork the repository
2. Create a new branch for your feature or bugfix
3. Make your changes
4. Add or update tests as necessary
5. Ensure all tests pass
6. Submit a pull request

## Development Setup

### Python

```bash
# Clone the repository
git clone https://github.com/yourusername/base64plus.git
cd base64plus

# Install in development mode with all OCR engines
python install.py --language python --ocr all --dev

# Generate test images
python install.py --test-image
```

### JavaScript

```bash
# Clone the repository
git clone https://github.com/yourusername/base64plus.git
cd base64plus

# Install in development mode
python install.py --language javascript --dev

# Generate test images
python install.py --test-image
```

## Project Structure

```
base64plus/
├── python/                 # Python implementation
│   ├── base64plus/         # Python package
│   ├── examples/           # Python examples
│   ├── setup.py            # Python package setup
│   └── README.md           # Python-specific documentation
├── javascript/             # JavaScript implementation
│   ├── examples/           # JavaScript examples
│   ├── index.js            # Main JavaScript implementation
│   ├── package.json        # Node.js package configuration
│   └── README.md           # JavaScript-specific documentation
├── tools/                  # Utility scripts
├── README.md               # Main project documentation
├── LICENSE                 # Project license
└── CONTRIBUTING.md         # Contribution guidelines
```

## Coding Standards

### Python

- Follow PEP 8 style guide
- Use docstrings for functions and classes
- Write unit tests for new functionality

### JavaScript

- Follow Standard JS style
- Use JSDoc comments for functions
- Write unit tests for new functionality

## Adding Support for New Languages

We welcome implementations in additional languages! If you'd like to add support for a new language:

1. Create a new directory for your language (e.g., `ruby/`, `go/`, etc.)
2. Implement the core functionality (encoding and decoding)
3. Create examples and documentation
4. Update the main README.md to include your implementation
5. Submit a pull request

## License

By contributing to Base64Plus, you agree that your contributions will be licensed under the project's MIT License.