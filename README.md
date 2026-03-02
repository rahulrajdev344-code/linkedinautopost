# 🚀 LinkedIn Auto Poster

Automatically generate and publish tech-related LinkedIn posts every 4 hours using **GitHub Actions** + **OpenRouter AI** (DeepSeek R1) + **LinkedIn API**.

Works **24/7** even when your laptop is off — everything runs in the cloud for free!

---

## ⚡ Quick Setup (15 minutes)

### Step 1: Get OpenRouter API Key (Free)

1. Go to [openrouter.ai/keys](https://openrouter.ai/keys)
2. Sign up / sign in
3. Create a new API key
4. Copy it — you'll need it in Step 4

### Step 2: Create LinkedIn Developer App

1. Go to [LinkedIn Developer Portal](https://www.linkedin.com/developers/apps)
2. Click **"Create App"**
3. Fill in:
   - **App name**: Auto Poster (or anything)
   - **LinkedIn Page**: Select or create one
   - **App logo**: Upload any image
4. Go to **Products** tab → Request access to:
   - ✅ **Share on LinkedIn**
   - ✅ **Sign In with LinkedIn using OpenID Connect**
5. Go to **Auth** tab → Add redirect URL: `http://localhost:8080/callback`
6. Note your **Client ID** and **Client Secret**

### Step 3: Get LinkedIn Access Token

```bash
# Install dependencies
pip install requests

# Edit the helper script — paste your Client ID and Client Secret
# Open helpers/get_linkedin_token.py and fill in CLIENT_ID and CLIENT_SECRET

# Run the token generator
python helpers/get_linkedin_token.py
```

This opens your browser → you authorize the app → you get an access token.

Then get your Person URN:
```bash
set LINKEDIN_ACCESS_TOKEN=<paste-your-token>
python helpers/get_person_urn.py
```

### Step 4: Push to GitHub & Add Secrets

1. Create a **private** GitHub repo
2. Push this code to it:
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin https://github.com/YOUR_USERNAME/linkedin-auto-poster.git
   git push -u origin main
   ```
3. Go to **Settings → Secrets and variables → Actions** → Add these secrets:

   | Secret Name | Value |
   |---|---|
   | `OPENROUTER_API_KEY` | Your OpenRouter API key |
   | `LINKEDIN_ACCESS_TOKEN` | The token from Step 3 |
   | `LINKEDIN_PERSON_URN` | The person ID from Step 3 |

### Step 5: Test It!

1. Go to **Actions** tab in your GitHub repo
2. Click **"Auto Post to LinkedIn"** workflow
3. Click **"Run workflow"** → set dry_run to `true` for a test
4. Check the logs — you should see a generated post
5. Run again with dry_run `false` to actually post!

---

## 📅 Schedule

Posts are published every **4 hours** automatically at:
- 00:00, 04:00, 08:00, 12:00, 16:00, 20:00 UTC

That's **6 posts per day**.

To change the frequency, edit `cron` in `.github/workflows/post-to-linkedin.yml`:
```yaml
# Every 6 hours
- cron: '0 */6 * * *'

# Every 8 hours
- cron: '0 */8 * * *'

# Once a day at 9 AM UTC
- cron: '0 9 * * *'
```

---

## 🎨 Customize Topics

Edit `config/topics.json` to add/remove/change the tech topics that posts are generated about.

---

## ⚠️ Important Notes

### LinkedIn Token Expiry
- Access tokens expire every **60 days**
- You'll need to re-run `helpers/get_linkedin_token.py` and update the GitHub secret
- Mark your calendar! Set a reminder for ~55 days

### OpenRouter Free Tier
- DeepSeek R1 is free on OpenRouter
- 6 requests/day is well within free limits
- No credit card required

### GitHub Actions Free Tier
- Public repos: unlimited minutes
- Private repos: 2,000 minutes/month (free)
- This workflow uses ~1 min/run = ~180 min/month — well within free limits

---

## 🛠 Troubleshooting

| Issue | Solution |
|---|---|
| Post not appearing on LinkedIn | Check if your access token has expired (re-run token helper) |
| "Unauthorized" error | Verify LINKEDIN_ACCESS_TOKEN secret is correct |
| Empty or weird post content | Check OpenRouter API key and model availability |
| GitHub Action not running | Make sure the workflow file is in `.github/workflows/` on `main` branch |
| Rate limiting | Reduce posting frequency in the cron schedule |

---

## 📁 Project Structure

```
├── .github/workflows/
│   └── post-to-linkedin.yml    # Cron scheduler (every 4 hrs)
├── scripts/
│   ├── generate_post.py        # AI content generation (OpenRouter)
│   ├── post_to_linkedin.py     # LinkedIn API posting
│   └── main.py                 # Orchestrator
├── helpers/
│   ├── get_linkedin_token.py   # One-time: Get OAuth token
│   └── get_person_urn.py       # One-time: Get your LinkedIn ID
├── config/
│   └── topics.json             # Tech topics to post about
├── requirements.txt
└── README.md
```
