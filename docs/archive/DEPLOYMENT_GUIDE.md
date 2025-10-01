# 🚀 Complete Deployment Guide

This guide provides step-by-step instructions to deploy your Emotiv LSL project to GitHub with full CI/CD integration.

## 📋 Prerequisites Checklist

Before you begin, ensure you have:

- [ ] Git installed and configured
- [ ] GitHub account created
- [ ] All code tested locally and working
- [ ] Virtual environment set up

## 🎯 Step-by-Step Deployment

### Step 1: Configure Git Identity (First Time Only)

```bash
cd /Users/yawningbrain/Desktop/emotiv-lsl-main

git config user.name "Your Name"
git config user.email "your.email@example.com"
```

### Step 2: Create GitHub Repository

**Option A: Using GitHub CLI (Recommended)**

```bash
# Install GitHub CLI if not already installed
brew install gh  # macOS

# Authenticate
gh auth login

# Create repository
gh repo create emotiv-lsl --public --description "Lab Streaming Layer server for Emotiv EPOC X EEG headset"
```

**Option B: Manual Creation**

1. Go to https://github.com/new
2. Repository name: `emotiv-lsl`
3. Description: "Lab Streaming Layer server for Emotiv EPOC X EEG headset"
4. Choose Public or Private
5. **DO NOT** initialize with README, .gitignore, or license (we already have these)
6. Click "Create repository"

### Step 3: Link Local Repository to GitHub

```bash
# Add remote (replace YOUR_USERNAME with your GitHub username)
git remote add origin https://github.com/YOUR_USERNAME/emotiv-lsl.git

# Verify remote was added
git remote -v
```

### Step 4: Push Code to GitHub

```bash
# Push main branch
git checkout main
git push -u origin main

# Push streamlit-app branch
git checkout streamlit-app
git push -u origin streamlit-app

# Verify branches are pushed
git branch -r
```

### Step 5: Verify GitHub Actions

1. Go to your repository on GitHub
2. Click the "Actions" tab
3. You should see workflows running automatically
4. Wait for all checks to complete (may take 3-5 minutes)

### Step 6: Enable Branch Protection (Recommended)

1. Go to repository Settings → Branches
2. Click "Add branch protection rule"
3. Branch name pattern: `main`
4. Enable:
   - ✅ Require a pull request before merging
   - ✅ Require status checks to pass before merging
   - ✅ Require branches to be up to date before merging
5. Save changes

## 🎨 Optional Enhancements

### Deploy Streamlit App to Cloud

1. Go to https://share.streamlit.io
2. Sign in with GitHub
3. Click "New app"
4. Select your repository
5. Branch: `streamlit-app`
6. Main file path: `streamlit_app.py`
7. Click "Deploy"

**Note**: Cloud deployment won't have hardware access, but great for demos!

### Set Up PyPI Publishing

1. Create account at https://pypi.org
2. Generate API token at https://pypi.org/manage/account/token/
3. Copy the token (starts with `pypi-`)
4. In GitHub: Settings → Secrets and variables → Actions
5. Click "New repository secret"
6. Name: `PYPI_API_TOKEN`
7. Value: Paste your token
8. Save

Now releases will automatically publish to PyPI!

### Add Status Badges to README

Add these to the top of your `README.md`:

```markdown
[![CI/CD](https://github.com/YOUR_USERNAME/emotiv-lsl/actions/workflows/ci.yml/badge.svg)](https://github.com/YOUR_USERNAME/emotiv-lsl/actions/workflows/ci.yml)
[![Python Version](https://img.shields.io/badge/python-3.9%2B-blue)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)
```

### Enable Codecov (Code Coverage)

1. Go to https://codecov.io
2. Sign in with GitHub
3. Add your repository
4. Copy the token
5. Add as GitHub Secret: `CODECOV_TOKEN`
6. Coverage reports will appear on PRs!

## 🔄 Making Changes and Updates

### Regular Development Workflow

```bash
# 1. Create a feature branch
git checkout -b feature/my-new-feature

# 2. Make your changes
# ... edit files ...

# 3. Commit changes
git add -A
git commit -m "Add: brief description of changes"

# 4. Push branch
git push -u origin feature/my-new-feature

# 5. Create Pull Request on GitHub
# Go to your repository and click "Compare & pull request"

# 6. Wait for CI checks to pass
# Merge when ready
```

### Creating a Release

```bash
# 1. Update version in pyproject.toml and setup.py
# 2. Update CHANGELOG.md

# 3. Commit version bump
git checkout main
git add pyproject.toml setup.py CHANGELOG.md
git commit -m "Bump version to 1.0.0"
git push origin main

# 4. Create and push tag
git tag v1.0.0
git push origin v1.0.0

# 5. GitHub Actions automatically:
#    - Runs all tests
#    - Builds package
#    - Creates GitHub release
#    - Publishes to PyPI (if configured)
```

## 🐛 Troubleshooting

### Push Rejected

```bash
# Error: Updates were rejected because the remote contains work...
# Solution: Pull first
git pull origin streamlit-app --rebase
git push origin streamlit-app
```

### CI Failing

1. Click on the failing workflow in Actions tab
2. Expand the failing step to see error details
3. Fix the issue locally
4. Commit and push again

### Can't Find Repository

```bash
# Check remote URL
git remote -v

# Update remote URL if needed
git remote set-url origin https://github.com/YOUR_USERNAME/emotiv-lsl.git
```

## 📊 Monitoring Your Project

### Key Metrics to Watch

1. **Build Status**: Green checks on all workflows
2. **Code Coverage**: Aim for >80%
3. **Security Alerts**: Review and fix promptly
4. **Dependencies**: Keep updated with Dependabot

### Regular Maintenance

- [ ] Review Dependabot PRs monthly
- [ ] Check GitHub Security advisories
- [ ] Update documentation as needed
- [ ] Tag releases for major milestones

## 🎓 Next Steps

After successful deployment:

1. ✅ **Test the Streamlit App**: `./run_app.sh`
2. ✅ **Invite Collaborators**: Settings → Collaborators
3. ✅ **Write Good Commit Messages**: Follow conventional commits
4. ✅ **Create Issues**: Track bugs and features
5. ✅ **Add Documentation**: Keep README.md updated

## 📚 Resources

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Streamlit Documentation](https://docs.streamlit.io)
- [Python Packaging Guide](https://packaging.python.org)
- [Git Best Practices](https://git-scm.com/book/en/v2)

## ✅ Deployment Checklist

Once deployed, verify:

- [ ] Both branches visible on GitHub
- [ ] GitHub Actions running successfully
- [ ] README displays properly
- [ ] All documentation files present
- [ ] Issues and Discussions enabled
- [ ] License file visible
- [ ] .gitignore working (no venv/ or data files in repo)

## 🎉 Success!

Your project is now professionally deployed with:

- ✨ Full CI/CD pipeline
- 🧪 Automated testing
- 🔒 Security scanning
- 📦 Release automation
- 🎨 Modern Streamlit UI
- 📚 Comprehensive documentation

**Share your project with the world! 🌍**

---

Need help? Check out [GITHUB_SETUP.md](GITHUB_SETUP.md) or open an issue!

