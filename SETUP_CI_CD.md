# CI/CD Setup Guide

This guide explains how to set up the enhanced CI/CD pipeline for git-tag-based semversioning and automated releases.

## 🚀 Quick Setup

### 1. Install Enhanced GitHub Actions Workflows

Due to GitHub App permissions, the enhanced workflows need to be installed manually:

```bash
# Navigate to your repository
cd /path/to/twat-search

# Install enhanced workflows (replace existing ones)
mv .github/workflows/push-enhanced.yml.template .github/workflows/push.yml
mv .github/workflows/release-enhanced.yml.template .github/workflows/release.yml
mv .github/workflows/pre-release.yml.template .github/workflows/pre-release.yml

# Commit the changes
git add .github/workflows/
git commit -m "feat: enhance CI/CD workflows with multiplatform support and semver validation"
```

### 2. Set Up GitHub Secrets

Configure the following secrets in your GitHub repository (Settings > Secrets and Variables > Actions):

#### Required Secrets:
- `PYPI_TOKEN` - PyPI API token for publishing releases
- `TEST_PYPI_TOKEN` - Test PyPI API token for pre-releases (optional)

#### Optional Secrets:
- `CODECOV_TOKEN` - Codecov token for coverage reporting (optional)

### 3. Configure GitHub Environments

Set up the following environments in your repository (Settings > Environments):

#### PyPI Environment:
- Name: `pypi`
- URL: `https://pypi.org/p/twat-search`
- Required reviewers: (optional, for manual approval)

#### Test PyPI Environment (optional):
- Name: `testpypi`
- URL: `https://test.pypi.org/p/twat-search`

## 📋 Feature Overview

### Enhanced Push Workflow (`push.yml`)
- **Multiplatform Testing**: Ubuntu, Windows, macOS
- **Python Version Matrix**: 3.10, 3.11, 3.12
- **Code Quality**: Ruff linting, formatting, MyPy type checking
- **Binary Builds**: Standalone executables for all platforms
- **Coverage Reporting**: Comprehensive test coverage analysis
- **Artifact Management**: Stores binaries and coverage reports

### Enhanced Release Workflow (`release.yml`)
- **Semver Validation**: Automatic semantic version validation
- **Comprehensive Testing**: Full test suite on release
- **Distribution Building**: Python packages and platform binaries
- **PyPI Publishing**: Automated package publishing
- **GitHub Releases**: Automatic release creation with assets
- **Release Notes**: Auto-generated from changelog

### Pre-Release Workflow (`pre-release.yml`)
- **Manual Trigger**: Workflow dispatch for testing
- **Test PyPI**: Publishes to Test PyPI for validation
- **GitHub Pre-Release**: Creates pre-release for testing
- **Version Validation**: Supports pre-release versions (e.g., 1.0.0-alpha.1)

## 🔧 Local Development Scripts

The repository includes three powerful local development scripts:

### Build Script (`scripts/build.sh`)
```bash
# Full build pipeline
./scripts/build.sh

# Only code quality checks
./scripts/build.sh --quality

# Only run tests
./scripts/build.sh --test

# Only build package
./scripts/build.sh --build

# Build without tests
./scripts/build.sh --skip-tests
```

### Test Script (`scripts/test.sh`)
```bash
# Run all tests
./scripts/test.sh

# Run unit tests only
./scripts/test.sh --unit

# Run integration tests only
./scripts/test.sh --integration

# Run specific test pattern
./scripts/test.sh --pattern "search"

# Run tests with specific marker
./scripts/test.sh --marker "unit"

# Generate comprehensive test report
./scripts/test.sh --report

# Run in watch mode for continuous testing
./scripts/test.sh --watch
```

### Release Script (`scripts/release.sh`)
```bash
# Release a new version
./scripts/release.sh 1.0.0

# Show current version
./scripts/release.sh --current

# Suggest next version
./scripts/release.sh --major   # Next major version
./scripts/release.sh --minor   # Next minor version
./scripts/release.sh --patch   # Next patch version

# Dry run (show what would be done)
./scripts/release.sh --dry-run 1.0.0

# Create release and push tags
./scripts/release.sh --push-tags 1.0.0
```

## 🎯 Release Process

### Regular Releases

1. **Ensure Clean State**:
   ```bash
   git checkout main
   git pull origin main
   ./scripts/build.sh  # Run full build and tests
   ```

2. **Create Release**:
   ```bash
   # Option 1: Use the release script
   ./scripts/release.sh 1.0.0

   # Option 2: Manual git tag
   git tag v1.0.0
   git push origin v1.0.0
   ```

3. **Automated Process**:
   - GitHub Actions validates the semver tag
   - Runs comprehensive tests on all platforms
   - Builds Python packages and binaries
   - Publishes to PyPI
   - Creates GitHub release with assets

### Pre-Releases

1. **Navigate to GitHub Actions**:
   - Go to your repository's Actions tab
   - Select "Pre-Release" workflow
   - Click "Run workflow"

2. **Configure Pre-Release**:
   - Enter version (e.g., `1.0.0-alpha.1`)
   - Choose whether to create git tag
   - Run the workflow

3. **Automated Process**:
   - Validates pre-release version format
   - Runs tests and builds packages
   - Publishes to Test PyPI
   - Creates GitHub pre-release

## 🔍 Troubleshooting

### Common Issues

1. **Workflow Permission Errors**:
   - Ensure GitHub App has sufficient permissions
   - Check repository settings for Actions permissions

2. **PyPI Publishing Failures**:
   - Verify `PYPI_TOKEN` is correctly set
   - Check if version already exists on PyPI

3. **Binary Build Failures**:
   - Ensure all dependencies are properly listed
   - Check PyInstaller configuration for platform-specific issues

4. **Test Failures**:
   - Run tests locally with `./scripts/test.sh`
   - Check for platform-specific issues in the matrix

### Debug Commands

```bash
# Check current git status
git status

# View recent commits
git log --oneline -10

# Check current version
./scripts/release.sh --current

# Run tests with verbose output
./scripts/test.sh --unit --verbose

# Build with verbose output
./scripts/build.sh --verbose
```

## 📊 Monitoring

### GitHub Actions Monitoring
- Monitor workflow runs in the Actions tab
- Check for failed runs and error messages
- Review artifact uploads and downloads

### Coverage Monitoring
- Coverage reports are generated for each test run
- HTML reports available in artifacts
- Codecov integration (if configured)

### Release Monitoring
- Monitor PyPI for successful package uploads
- Check GitHub releases for proper asset uploads
- Verify binary functionality across platforms

## 🔐 Security Considerations

### Secrets Management
- Use GitHub repository secrets for sensitive data
- Never commit API tokens to the repository
- Regularly rotate API tokens

### Workflow Security
- Review workflow permissions regularly
- Use pinned action versions for security
- Monitor for security advisories

### Binary Security
- Binaries are built in isolated environments
- Consider code signing for production releases
- Verify binary integrity before distribution

## 🚀 Advanced Configuration

### Custom Environments
You can create additional environments for staging, testing, etc.:

```yaml
# In your workflow file
environment:
  name: staging
  url: https://staging.example.com
```

### Matrix Customization
Modify the test matrix in workflows for different configurations:

```yaml
strategy:
  matrix:
    python-version: ["3.10", "3.11", "3.12"]
    os: [ubuntu-latest, windows-latest, macos-latest]
    include:
      - python-version: "3.13"
        os: ubuntu-latest
```

### Custom Build Steps
Add custom build steps for specific requirements:

```yaml
- name: Custom Build Step
  run: |
    echo "Running custom build logic"
    # Your custom commands here
```

## 📖 Additional Resources

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [PyPI Publishing Guide](https://packaging.python.org/guides/publishing-package-distribution-releases-using-github-actions-ci-cd-workflows/)
- [Semantic Versioning](https://semver.org/)
- [Hatch Documentation](https://hatch.pypa.io/)
- [UV Documentation](https://github.com/astral-sh/uv)

## 🤝 Support

If you encounter issues with the CI/CD setup:

1. Check the troubleshooting section above
2. Review GitHub Actions logs for specific errors
3. Test locally using the provided scripts
4. Open an issue with detailed error information

The enhanced CI/CD pipeline provides a robust foundation for automated testing, building, and releasing your Python packages with comprehensive multiplatform support.