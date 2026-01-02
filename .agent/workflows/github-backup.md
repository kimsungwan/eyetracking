---
description: How to backup the project to GitHub
---

This workflow guides you through the process of backing up your current project state to a GitHub repository.

## Prerequisites
- A GitHub account
- Git installed on your machine (already installed)

## Steps

1. **Create a new repository on GitHub**
   - Go to [https://github.com/new](https://github.com/new)
   - Enter a repository name (e.g., `koreansaas-backup`)
   - Choose **Private** (recommended for backups)
   - Do **NOT** initialize with README, .gitignore, or License (keep it empty)
   - Click **Create repository**

2. **Connect your local project to GitHub**
   - Copy the URL of your new repository (e.g., `https://github.com/your-username/koreansaas-backup.git`)
   - Run the following command in your terminal (replace the URL with yours):

   ```bash
   git remote add origin https://github.com/your-username/koreansaas-backup.git
   ```
   *(If `origin` already exists, use `git remote set-url origin <URL>` instead)*

3. **Push your code**
   - Run the following command to upload your code:

   ```bash
   git push -u origin main
   ```

4. **Verify**
   - Refresh your GitHub repository page to see your files.

> [!TIP]
> You can run this workflow anytime you want to save your progress to the cloud.
> Just run `git add .`, `git commit -m "message"`, and then `git push`.
