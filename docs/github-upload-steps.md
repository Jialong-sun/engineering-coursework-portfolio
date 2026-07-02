# GitHub Upload Steps

Recommended repository name:

```text
engineering-coursework-portfolio
```

After creating an empty GitHub repository with that name, run these commands from this folder:

```powershell
git init
git add .
git commit -m "Initial curated engineering coursework portfolio"
git branch -M main
git remote add origin https://github.com/<your-username>/engineering-coursework-portfolio.git
git push -u origin main
```

If Git asks for identity information, set it locally inside this repository:

```powershell
git config user.name "Jialong Sun"
git config user.email "<your-email@example.com>"
```

Before publishing, do one final review to confirm no raw coursework documents, student IDs, classmates' names, private files, or screenshots with personal data were added.
