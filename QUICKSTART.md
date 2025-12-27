# Quick Setup Guide - Vercel Auto-Deploy

## ⚡ Fast Setup (5 minutes)

### 1. Get Your Vercel Deploy Hook

Visit: https://vercel.com/dashboard
→ Select `kahvila` project
→ Settings → Git → Deploy Hooks
→ Create Hook (name: "Wolt Updates", branch: "main")
→ Copy the URL

### 2. Edit config.json

Replace these two values:

```json
{
  "wolt_url": "YOUR_WOLT_PAGE_URL",
  "vercel_deploy_hook": "PASTE_DEPLOY_HOOK_URL"
}
```

### 3. Save and Push

```bash
git add config.json
git commit -m "Configure crawler"
git push origin main
```

### 4. Run the Crawler

Double-click: `run_crawler.bat`

## ✅ Done!

Now when you update your Wolt menu:
- Crawler detects changes
- Updates products.json
- Pushes to GitHub
- Triggers Vercel deployment
- Live site updates automatically!

## 🌐 Your Sites

- **Live Website**: https://kahvila-ochre.vercel.app/
- **GitHub Repo**: https://github.com/amir-android123/kahvila
- **Vercel Dashboard**: https://vercel.com/dashboard

---

**Need detailed instructions?** See [VERCEL_SETUP.md](VERCEL_SETUP.md)
