# GitHub Setup Guide

This guide will help you set up this repository on GitHub with full CI/CD integration.

## 🚀 Quick Setup

### 1. Create GitHub Repository

```bash
# Option A: Using GitHub CLI (recommended)
gh repo create emotiv-lsl --public --source=. --remote=origin

# Option B: Create repository manually on GitHub.com
# Then link it:
git remote add origin https://github.com/YOUR_USERNAME/emotiv-lsl.git
```

### 2. Push Code to GitHub

```bash
# Push both branches
git push -u origin main
git push -u origin streamlit-app
```

### 3. Enable GitHub Actions

GitHub Actions will automatically run when you push code. No additional setup needed!

## 🔧 Optional: Advanced Configuration

### Set up PyPI Publishing (for releases)

1. Go to https://pypi.org/manage/account/token/
2. Create an API token
3. In your GitHub repo, go to Settings → Secrets → Actions
4. Add secret: `PYPI_API_TOKEN` with your token

### Set up Streamlit Cloud Deployment

1. Go to https://share.streamlit.io
2. Sign in with GitHub
3. Deploy from the `streamlit-app` branch
4. Select `streamlit_app.py` as the main file

### Enable GitHub Pages (for documentation)

1. Go to Settings → Pages
2. Source: Deploy from a branch
3. Branch: `main` → `/docs` folder
4. Save

## 📋 CI/CD Workflows

### Main CI Pipeline (`ci.yml`)
Runs on every push and pull request:
- ✅ Linting (Black, isort, Flake8, Pylint)
- ✅ Testing (pytest across multiple OS and Python versions)
- ✅ Security scanning (Safety, Bandit)
- ✅ Build verification
- ✅ Documentation check

### Release Pipeline (`release.yml`)
Triggers on version tags (e.g., `v1.0.0`):
- 📦 Builds Python package
- 📝 Creates GitHub release with changelog
- 🚀 Publishes to PyPI (if configured)

### Streamlit Deploy (`streamlit-deploy.yml`)
Runs when `streamlit_app.py` changes:
- ✅ Validates Streamlit app syntax
- 📢 Deployment notification

## 🏷️ Creating a Release

```bash
# Update version in setup.py and pyproject.toml
git add .
git commit -m "Bump version to 1.0.0"

# Create and push tag
git tag v1.0.0
git push origin v1.0.0

# GitHub Actions will automatically:
# - Run all tests
# - Build package
# - Create GitHub release
# - Publish to PyPI (if configured)
```

## 🔒 Security Best Practices

1. **Never commit secrets** - Use GitHub Secrets for sensitive data
2. **Enable branch protection** - Require PR reviews and status checks
3. **Keep dependencies updated** - Dependabot will create PRs automatically
4. **Review security alerts** - GitHub will notify you of vulnerabilities

## 📊 Status Badges

Add these to your README.md:

```markdown
[![CI/CD](https://github.com/YOUR_USERNAME/emotiv-lsl/actions/workflows/ci.yml/badge.svg)](https://github.com/YOUR_USERNAME/emotiv-lsl/actions/workflows/ci.yml)
[![codecov](https://codecov.io/gh/YOUR_USERNAME/emotiv-lsl/branch/main/graph/badge.svg)](https://codecov.io/gh/YOUR_USERNAME/emotiv-lsl)
[![PyPI](https://img.shields.io/pypi/v/emotiv-lsl.svg)](https://pypi.org/project/emotiv-lsl/)
[![Python Version](https://img.shields.io/pypi/pyversions/emotiv-lsl.svg)](https://pypi.org/project/emotiv-lsl/)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)
```

## 🐛 Troubleshooting

### CI Fails on macOS Runner

If tests fail on macOS due to LSL library:
- This is expected (no hardware available in CI)
- Tests are marked `continue-on-error: true`
- Focus on passing Linux tests

### PyPI Publishing Fails

- Ensure `PYPI_API_TOKEN` secret is set
- Verify package name is available on PyPI
- Check version number hasn't been used before

### Streamlit Deploy Not Working

- Ensure you're deploying from `streamlit-app` branch
- Check that `streamlit_app.py` is in the root directory
- Verify all dependencies are in `requirements.txt`

## 📚 Additional Resources

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [PyPI Publishing Guide](https://packaging.python.org/guides/publishing-package-distribution-releases-using-github-actions-ci-cd-workflows/)
- [Streamlit Cloud Documentation](https://docs.streamlit.io/streamlit-cloud)

## 🤝 Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for development workflow and guidelines.

