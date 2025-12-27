# Vercel Auto-Deploy Setup Guide

This guide will help you set up automatic Vercel deployments when your Wolt products change.

## 🎯 What This Does

When the crawler detects changes to your Wolt menu:
1. ✅ Updates `products.json`
2. ✅ Commits and pushes to GitHub
3. ✅ Triggers Vercel to redeploy your website
4. ✅ Your live site updates automatically!

## 📋 Setup Steps

### Step 1: Create a Vercel Deploy Hook

1. Go to your Vercel project dashboard: https://vercel.com/dashboard
2. Select your project: `kahvila`
3. Go to **Settings** → **Git** → **Deploy Hooks**
4. Click **Create Hook**
5. Give it a name: `Wolt Product Updates`
6. Select branch: `main`
7. Click **Create Hook**
8. **Copy the webhook URL** (it looks like: `https://api.vercel.com/v1/integrations/deploy/...`)

### Step 2: Configure the Crawler

1. Open `config.json` in your project
2. Update the following values:

```json
{
  "wolt_url": "YOUR_ACTUAL_WOLT_RESTAURANT_URL",
  "output_file": "products.json",
  "check_interval_minutes": 5,
  "log_file": "crawler.log",
  "vercel_deploy_hook": "PASTE_YOUR_VERCEL_DEPLOY_HOOK_URL_HERE"
}
```

Example:
```json
{
  "wolt_url": "https://wolt.com/en/fin/helsinki/restaurant/bon-bon",
  "output_file": "products.json",
  "check_interval_minutes": 5,
  "log_file": "crawler.log",
  "vercel_deploy_hook": "https://api.vercel.com/v1/integrations/deploy/prj_xxxxx/xxxxx"
}
```

### Step 3: Commit Configuration

```bash
git add config.json
git commit -m "Configure Vercel auto-deploy"
git push origin main
```

### Step 4: Run the Crawler

Double-click `run_crawler.bat` or run:
```bash
python wolt_crawler.py
```

## 🎉 How It Works

```
┌─────────────────────┐
│  Wolt Menu Changes  │
└──────────┬──────────┘
           │
           ↓
┌─────────────────────┐
│  Crawler Detects    │
│  New Products       │
└──────────┬──────────┘
           │
           ↓
┌─────────────────────┐
│  Updates JSON File  │
└──────────┬──────────┘
           │
           ↓
┌─────────────────────┐
│  Commits to GitHub  │
└──────────┬──────────┘
           │
           ↓
┌─────────────────────┐
│  Triggers Vercel    │
│  Deploy Hook        │
└──────────┬──────────┘
           │
           ↓
┌─────────────────────┐
│  Vercel Rebuilds    │
│  & Deploys Website  │
└──────────┬──────────┘
           │
           ↓
┌─────────────────────┐
│  Live Site Updated! │
│  kahvila-ochre      │
│  .vercel.app        │
└─────────────────────┘
```

## ⚙️ Configuration Options

| Option | Description | Default |
|--------|-------------|---------|
| `wolt_url` | Your Wolt restaurant page URL | Required |
| `output_file` | JSON file for products | `products.json` |
| `check_interval_minutes` | Minutes between checks | `5` |
| `vercel_deploy_hook` | Vercel deploy webhook URL | Optional |

## 🔍 Verification

When the crawler runs, you should see:

```
[2025-12-26 10:30:00] Checking for updates...
✓ New items added: Cappuccino, Croissant
✓ Updated! Total products: 15
📤 Committing and pushing to GitHub...
✓ Changes pushed to GitHub!
🚀 Triggering Vercel deployment...
✓ Vercel deployment triggered successfully!
```

Then check:
1. Your GitHub repo - should show a new commit
2. Vercel dashboard - should show a new deployment
3. Your live site - should show the new products in ~1-2 minutes

## 🚨 Troubleshooting

### Deploy Hook Not Working

**Check:**
- Is the deploy hook URL correct in `config.json`?
- Does the URL start with `https://api.vercel.com/v1/integrations/deploy/`?
- Is your Vercel project connected to the GitHub repo?

**Test manually:**
```bash
curl -X POST "YOUR_DEPLOY_HOOK_URL"
```

### Git Push Failing

**Check:**
- Are you authenticated with GitHub?
- Do you have push permissions?
- Is the git repo initialized?

**Fix:**
```bash
git config --global user.email "you@example.com"
git config --global user.name "Your Name"
```

### Products Not Showing on Live Site

**Check:**
- Is `products.json` in your GitHub repo?
- Did Vercel deployment complete successfully?
- Clear your browser cache
- Check browser console for errors

## 📱 Monitoring

View logs in real-time:
- **Crawler logs**: Check terminal output
- **Git activity**: Check GitHub commits
- **Vercel deployments**: Check Vercel dashboard
- **Live site**: https://kahvila-ochre.vercel.app/

## 🔐 Security Notes

- Keep your deploy hook URL private
- Don't commit it to public repos (use environment variables in production)
- The deploy hook can trigger deployments without authentication
- Consider using Vercel's build protection features

## ⏰ Recommended Settings

For a production cafe website:
- `check_interval_minutes`: `5-10` (don't check too frequently)
- Keep the crawler running on a dedicated server or local machine
- Monitor the `crawler.log` file for issues

## 🎯 Next Steps

1. ✅ Set up your Wolt URL
2. ✅ Create and configure Vercel deploy hook
3. ✅ Test the system with a manual product change
4. ✅ Set up the crawler to run automatically (Task Scheduler on Windows)
5. ✅ Monitor the first few deployments

## 💡 Tips

- The crawler needs to stay running to detect changes
- Use Windows Task Scheduler to start the crawler on system startup
- Check `crawler.log` periodically for any issues
- Vercel deployments take 30-60 seconds typically
- You get 100 GB-hours of build time per month on Vercel's free plan

---

**Need Help?** Check the main [CRAWLER_README.md](CRAWLER_README.md) for more details.
