# 🔒 Security Setup Guide

This guide explains how to securely store your sudo password for the Streamlit app.

## ⚠️ Important Security Notice

Storing your password in a file should **only be done on a personal machine you trust**. Never do this on:
- Shared computers
- Work machines
- Public/lab computers
- Servers accessible by others

## 📋 Setup Steps

### Step 1: Create Your `.env` File

```bash
cd /Users/yawningbrain/Desktop/emotiv-lsl-main

# Copy the example file
cp env.example .env
```

### Step 2: Edit the `.env` File

Open `.env` in your text editor:

```bash
nano .env
# or
open -e .env
```

Replace `your_password_here` with your actual macOS password:

```bash
# BEFORE
SUDO_PASSWORD=your_password_here

# AFTER (example)
SUDO_PASSWORD=MyActualPassword123
```

### Step 3: Secure the File

Make sure only you can read the file:

```bash
chmod 600 .env
```

This ensures only the owner (you) can read/write the file.

### Step 4: Verify It's Ignored by Git

Check that `.env` won't be committed:

```bash
git status
```

You should **NOT** see `.env` in the list of files. If you do, **STOP** and check `.gitignore`.

### Step 5: Test the App

```bash
./run_app.sh
```

Now you should be able to click "Start Server" without entering a password!

---

## 🔍 How It Works

### What Happens When You Start the Server

1. Streamlit app loads `.env` file
2. Reads `SUDO_PASSWORD` environment variable
3. Uses `sudo -S` (read password from stdin)
4. Sends password automatically
5. Server starts without prompting you

### Code Flow

```python
# streamlit_app.py
from dotenv import load_dotenv
load_dotenv()  # Loads .env file

sudo_password = os.getenv('SUDO_PASSWORD', '')
if sudo_password:
    # Use password from .env
    process = subprocess.Popen(
        ['sudo', '-S', ...],
        stdin=subprocess.PIPE
    )
    process.stdin.write(f"{sudo_password}\n")
```

---

## ✅ Security Checklist

- [ ] `.env` file created and configured
- [ ] `.env` file permissions set to 600 (read/write owner only)
- [ ] `.env` is listed in `.gitignore`
- [ ] Confirmed `.env` does NOT appear in `git status`
- [ ] Only used on personal, trusted machine
- [ ] Password never shared or displayed

---

## 🔐 Alternative: Passwordless Sudo (More Secure)

Instead of storing your password, you can configure passwordless sudo for specific commands:

### Option 1: All Sudo Commands (Simplest)

```bash
sudo visudo
```

Add this line (replace `yawningbrain` with your username):
```
yawningbrain ALL=(ALL) NOPASSWD: ALL
```

### Option 2: Specific Commands Only (More Secure)

```bash
sudo visudo
```

Add these lines:
```
yawningbrain ALL=(ALL) NOPASSWD: /usr/bin/killall
yawningbrain ALL=(ALL) NOPASSWD: /usr/bin/pkill
yawningbrain ALL=(ALL) NOPASSWD: /Users/yawningbrain/Desktop/emotiv-lsl-main/venv/bin/python
```

This allows passwordless sudo only for the specific commands the app needs.

---

## 🚨 If `.env` Gets Committed by Accident

### Step 1: Remove from Git History

```bash
# Remove the file from git (keeps local copy)
git rm --cached .env

# Commit the removal
git commit -m "Remove .env from git tracking"
```

### Step 2: Change Your Password

If you already pushed to GitHub:
1. **Change your macOS password immediately**
2. Update your `.env` file with the new password
3. Consider the old password compromised

### Step 3: Remove from GitHub History (if pushed)

```bash
# Use git filter-branch to remove from history
git filter-branch --force --index-filter \
  'git rm --cached --ignore-unmatch .env' \
  --prune-empty --tag-name-filter cat -- --all

# Force push (be careful!)
git push origin --force --all
```

⚠️ **Warning**: This rewrites history. Coordinate with collaborators if any.

---

## 🛡️ Best Practices

### DO ✅
- Use `.env` only on personal machines
- Set file permissions to 600
- Use strong passwords
- Review `.gitignore` regularly
- Consider passwordless sudo for specific commands

### DON'T ❌
- Share your `.env` file
- Commit `.env` to git
- Use this on shared/public machines
- Store passwords in plain text unnecessarily
- Use weak passwords

---

## 🔄 Without `.env` File

If you prefer not to store your password at all, the app will fall back to:

1. **Try passwordless sudo** (requires configuration)
2. **Fail gracefully** with a helpful error message
3. **Suggest manual server start** in separate terminal

This is the most secure option but less convenient.

---

## 📊 Security Comparison

| Method | Security | Convenience | Setup |
|--------|----------|-------------|-------|
| `.env` file | ⚠️ Medium | ⭐⭐⭐ High | Easy |
| Passwordless sudo (all) | ⚠️ Medium | ⭐⭐⭐ High | Easy |
| Passwordless sudo (specific) | ✅ Good | ⭐⭐⭐ High | Medium |
| Manual password entry | ✅ Best | ⭐ Low | None |
| Separate terminal | ✅ Best | ⭐⭐ Medium | None |

---

## 🆘 Troubleshooting

### `.env` file not working

**Check file location:**
```bash
ls -la /Users/yawningbrain/Desktop/emotiv-lsl-main/.env
```

**Check file contents:**
```bash
cat .env
```

**Check permissions:**
```bash
ls -l .env
# Should show: -rw------- (600)
```

### Password still being requested

- Ensure `.env` file is in the project root
- Check for typos in your password
- Verify `python-dotenv` is installed: `pip list | grep dotenv`
- Restart the Streamlit app

### App can't find `.env`

- File must be named exactly `.env` (not `env.txt` or `.env.txt`)
- File must be in the same directory as `streamlit_app.py`
- Use absolute path if needed

---

## 📚 Related Documentation

- [Streamlit App Guide](STREAMLIT_APP.md)
- [Getting Started](GETTING_STARTED.md)
- [Deployment Guide](DEPLOYMENT_GUIDE.md)

---

## ✨ Quick Setup Commands

```bash
# Complete setup in one go
cd /Users/yawningbrain/Desktop/emotiv-lsl-main
cp env.example .env
nano .env  # Edit and save your password
chmod 600 .env
git status  # Verify .env is not tracked
./run_app.sh  # Test!
```

---

**Remember**: Security is about balancing convenience with risk. Choose the method that works best for your situation! 🔐

