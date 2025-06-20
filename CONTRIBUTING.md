# Contributing to Streamlit Expandable Columns

Thank you for your interest in contributing to Streamlit Expandable Columns! This document provides guidelines and information for contributors.

## 🚀 Getting Started

### Prerequisites

- Python 3.9+
- Node.js 18+
- npm or yarn
- Git

### Development Setup

1. **Fork and clone the repository:**
   ```bash
   git clone https://github.com/your-username/streamlit-expandable-columns.git
   cd streamlit-expandable-columns
   ```

2. **Set up the development environment:**
   ```bash
   # Create virtual environment
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   
   # Install Python dependencies
   pip install -e ".[dev]"
   
   # Install frontend dependencies
   cd streamlit_expandable_columns/frontend
   npm install
   cd ../..
   ```

3. **Start development servers:**
   ```bash
   # Terminal 1: Frontend dev server
   cd streamlit_expandable_columns/frontend
   npm start
   
   # Terminal 2: Streamlit app
   source venv/bin/activate
   streamlit run example.py
   ```

## 🧪 Testing

### Running Tests

```bash
# Run all tests
make test

# Run only unit tests
make test-unit

# Run only E2E tests
make test-e2e

# Run with coverage
pytest --cov=streamlit_expandable_columns
```

### Test Structure

- **Unit Tests** (`tests/test_unit.py`): Test core functionality and API
- **Integration Tests** (`tests/test_integration.py`): Test Streamlit integration
- **E2E Tests** (`tests/test_*.py`): Test user interactions and visual elements
- **Test Apps** (`tests/streamlit_apps/`): Streamlit applications for testing

## 🔧 Development Workflow

### Code Quality

```bash
# Format code
make format

# Check linting
make lint

# Run full check
make format && make lint && make test
```

### Making Changes

1. **Create a feature branch:**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes:**
   - Follow the existing code style
   - Add tests for new functionality
   - Update documentation as needed

3. **Test your changes:**
   ```bash
   make test
   make format
   make lint
   ```

4. **Commit your changes:**
   ```bash
   git add .
   git commit -m "Add your feature description"
   ```

5. **Push and create a Pull Request:**
   ```bash
   git push origin feature/your-feature-name
   ```

## 📝 Code Style

### Python

- Follow PEP 8 style guidelines
- Use type hints where appropriate
- Write docstrings for all public functions
- Keep functions focused and concise

### JavaScript/React

- Use modern ES6+ syntax
- Follow React best practices
- Use meaningful variable and function names
- Add comments for complex logic

### Documentation

- Update README.md for user-facing changes
- Update docstrings for API changes
- Add examples for new features
- Keep documentation clear and concise

## 🐛 Bug Reports

When reporting bugs, please include:

1. **Environment information:**
   - Python version
   - Streamlit version
   - Operating system
   - Browser (if relevant)

2. **Steps to reproduce:**
   - Clear, step-by-step instructions
   - Minimal code example

3. **Expected vs actual behavior:**
   - What you expected to happen
   - What actually happened

4. **Additional context:**
   - Error messages
   - Screenshots (if relevant)
   - Console logs

## 💡 Feature Requests

When suggesting features:

1. **Describe the problem:**
   - What are you trying to accomplish?
   - What limitations are you encountering?

2. **Propose a solution:**
   - How would you like to see this implemented?
   - Any specific requirements or constraints?

3. **Consider alternatives:**
   - Are there existing ways to achieve this?
   - What are the trade-offs?

## 🔄 Pull Request Process

1. **Ensure tests pass:**
   - All existing tests should pass
   - Add tests for new functionality
   - Update tests for changed functionality

2. **Check code quality:**
   - Code is properly formatted
   - Linting passes
   - No obvious issues

3. **Update documentation:**
   - README.md for user-facing changes
   - Docstrings for API changes
   - Examples for new features

4. **Write a clear description:**
   - What the PR does
   - Why the changes are needed
   - Any breaking changes

5. **Request review:**
   - Tag relevant maintainers
   - Provide context for reviewers

## 📋 Issue Labels

- `bug`: Something isn't working
- `enhancement`: New feature or request
- `documentation`: Improvements or additions to documentation
- `good first issue`: Good for newcomers
- `help wanted`: Extra attention is needed
- `question`: Further information is requested

## 🎯 Development Priorities

1. **Bug fixes** - Critical issues affecting functionality
2. **Documentation** - Improving user experience
3. **Performance** - Optimizing existing features
4. **New features** - Adding requested functionality
5. **Refactoring** - Improving code quality

## 🚀 Release Process

This section outlines the steps to prepare the streamlit-expandable-columns package for release.

### 🧪 Testing Infrastructure

The project includes a comprehensive test suite:
- **Unit Tests** (`tests/test_unit.py`): Test core functionality and API
- **Integration Tests** (`tests/test_integration.py`): Test Streamlit integration
- **E2E Tests**: Test user interactions and visual elements for all major features
- **Test Utilities** (`tests/e2e_utils.py`): Shared testing utilities
- **Test Apps** (`tests/streamlit_apps/`): Streamlit applications for testing

### 🔧 Development Infrastructure

The project includes:
- **Development tools**: `Makefile` with common tasks, `requirements-dev.txt`
- **Code quality tools**: black, flake8, isort
- **Package configuration**: Updated `setup.py` with test dependencies
- **GitHub Actions workflow**: Automated testing and quality checks

### 📖 Documentation

Before release, ensure:
- README.md is updated with comprehensive examples
- Development setup instructions are current
- Testing documentation is complete
- Contributing guidelines are up to date

### 🚀 Release Commands

#### Install Development Environment
```bash
# Install with development dependencies
make install-dev

# Or manually:
pip install -e ".[dev]"
pip install -r requirements-dev.txt
playwright install
```

#### Run Tests
```bash
# All tests
make test

# Unit tests only
make test-unit

# E2E tests only
make test-e2e
```

#### Code Quality
```bash
# Format code
make format

# Check linting
make lint
```

#### Version Management
```bash
# Update version (patch, minor, or major)
bump-my-version bump patch  # or minor, major

# This automatically updates:
# - setup.py version
# - frontend/package.json version
# - README.md version references
# - __init__.py __version__
```

#### Build and Release
```bash
# Build package
make build

# Upload to PyPI (requires PyPI credentials)
make upload
```

### 📋 Pre-Release Checklist

Before releasing:

- [ ] All tests pass locally (`make test`)
- [ ] Code is properly formatted (`make format`)
- [ ] Linting passes (`make lint`)
- [ ] GitHub Actions workflow passes
- [ ] Version number updated using `bump-my-version`
- [ ] CHANGELOG updated with new version
- [ ] README examples tested manually
- [ ] Frontend built and tested (`npm run build`)
- [ ] Package installs correctly from source

### 🎯 Test Coverage

The test suite covers:

#### Unit Tests
- Component initialization
- Parameter validation
- Session state management
- Width calculations
- Return value structures

#### Integration Tests  
- Streamlit integration
- State persistence
- Parameter forwarding
- Error handling
- Key uniqueness

#### E2E Tests
- Component rendering
- Resize handle functionality
- Label display
- Width ratios
- Custom parameters
- User interactions

#### Cross-Browser Support
- Firefox testing
- Chromium testing
- Headless mode for CI/CD

### 🔄 Continuous Integration

GitHub Actions workflow runs:
- Python 3.9, 3.10, 3.11 compatibility
- Linting and formatting checks
- Unit and E2E tests
- Package building validation
- Cross-browser testing

### ✅ Release Ready

The package is ready for release when it has:
- ✅ Clean codebase without personal information
- ✅ Comprehensive test coverage
- ✅ Professional development infrastructure
- ✅ Automated testing and quality checks
- ✅ Clear documentation and examples

## 📞 Getting Help

- **GitHub Issues:** For bugs and feature requests
- **GitHub Discussions:** For questions and general discussion
- **Documentation:** Check README.md and example files first

## 📄 License

By contributing, you agree that your contributions will be licensed under the MIT License.

Thank you for contributing! 🎉 