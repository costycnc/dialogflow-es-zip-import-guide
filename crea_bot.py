"""
GitHub Project Generator
Dialogflow ES - ZIP Import Guide
Creates all files in a folder ready to push to GitHub
"""
import os
import json
import zipfile
import shutil
import uuid

# ==========================================
# CONFIGURATION
# ==========================================
PROJECT_DIR = "dialogflow-es-zip-import-guide"
ZIP_NAME = "dialogflow-es-chatbot.zip"
AGENT_NAME = "costycnc-bot"

# ==========================================
# BOT INTENTS
# ==========================================
intents = [
    {
        "name": "greeting",
        "phrases": ["hello", "hi", "hey", "good morning", "good evening"],
        "responses": ["Hello! I am the CostyCNC virtual assistant.\nI can help you with:\n- SVG to G-code conversion\n- CNC machine information\n- Prices and shipping\n- Software installation\n\nHow can I help you?"]
    },
    {
        "name": "goodbye",
        "phrases": ["goodbye", "bye", "see you", "farewell"],
        "responses": ["Goodbye! Come back anytime.\nHappy cutting with CostyCNC!"]
    },
    {
        "name": "thanks",
        "phrases": ["thanks", "thank you", "thanks a lot", "much appreciated"],
        "responses": ["You're welcome! I'm here if you have more questions."]
    },
    {
        "name": "confirm_yes",
        "phrases": ["yes", "yeah", "ok", "sure", "of course", "correct", "right"],
        "responses": ["Great! Just tell me what you need."]
    },
    {
        "name": "confirm_no",
        "phrases": ["no", "no thanks", "not interested", "nope"],
        "responses": ["Alright! I'm here if you change your mind."]
    },
    {
        "name": "svg_to_gcode",
        "phrases": [
            "how do I convert svg to gcode",
            "svg to gcode",
            "convert svg to gcode",
            "how to convert svg to gcode",
            "i have an svg file how do i turn it into gcode",
            "transform svg to gcode"
        ],
        "responses": ["To convert SVG to G-code use the CostyCNC tool:\n\n1. Go to https://www.costycnc.it/cm8\n2. Click 'Paste SVG from Inkscape'\n3. Paste your SVG (Ctrl+V)\n4. Adjust size and DPI\n5. Click 'Create GCODE'\n6. Save with 'Save gcode'\n\nThe tool is free and runs in your browser!"]
    },
    {
        "name": "image_to_gcode",
        "phrases": [
            "how do I convert an image to gcode",
            "image to gcode",
            "convert jpg to gcode",
            "convert png to gcode",
            "how to turn a picture into gcode"
        ],
        "responses": ["To convert an image to G-code:\n\n1. Go to https://www.costycnc.it/cm8\n2. Load your image (JPG, PNG, BMP, SVG)\n3. Adjust DPI and size\n4. Click 'Create GCODE'\n\nThe tool extracts paths and optimizes them automatically."]
    },
    {
        "name": "Info_Prices",
        "phrases": [
            "how much does it cost", "what is the price", "prices",
            "how much is it", "price list", "cost of the machine"
        ],
        "responses": ["Here are the prices of our CostyCNC machines:\n\nHOBBY  - 150x30x8 cm  - from 125 EUR\nMINI   - 150x40x15 cm - from 210 EUR\nMEDIA  - 250x50x30 cm - from 410 EUR\nXBIG   - 250x90x90 cm - from 600 EUR\n\nPrices vary by destination.\nDetails: https://www.costycnc.it"]
    },
    {
        "name": "info_software_installation",
        "phrases": [
            "how do I install the software", "installation",
            "how to install", "do I need to install something",
            "program to download"
        ],
        "responses": ["The CostyCNC software is offline and free:\n\n1. Go to https://www.costycnc.it/cm8\n2. Download 'costycnc-img-to-gcode.zip'\n3. Extract the file\n4. Open 'index.html' in your browser\n\nNo installation needed!"]
    },
    {
        "name": "info_firmware",
        "phrases": ["firmware", "what firmware", "update firmware", "grbl", "mks dlc32"],
        "responses": ["Our machines use:\n- Board: MKS DLC32\n- Firmware: GRBL compatible\n- Connection: WiFi, USB, SD\n\nLatest firmware:\nhttps://www.costycnc.it/firmware"]
    },
    {
        "name": "info_specs",
        "phrases": ["specifications", "tech specs", "working area", "what motors", "control board"],
        "responses": ["CostyCNC technical specifications:\n\n- Motors: 28BYJ-48 / NEMA 17\n- Driver: A4988\n- Board: MKS DLC32 (WiFi + USB + SD)\n- Hot wire: Nichrome 0.2mm\n- Power: 12V or 24V"]
    },
    {
        "name": "info_cutting_foam",
        "phrases": ["what materials can it cut", "can I cut foam", "cut polystyrene", "cutting thickness", "hot wire cutting"],
        "responses": ["Our machines cut:\n- Polystyrene (EPS)\n- Extruded polystyrene (XPS)\n- Lightweight foam materials\n\nCutting is done with a hot wire."]
    },
    {
        "name": "info_rotary_table",
        "phrases": ["rotary table", "rotating table", "can I cut round shapes"],
        "responses": ["Yes! CostyCNC supports a rotary table for:\n- Cylindrical shapes\n- Cones and spheres\n- 3D shapes with rotation\n\nIt is activated from the 'Rotate Table' panel in the software."]
    },
    {
        "name": "info_shipping",
        "phrases": ["do you ship", "shipping", "delivery time", "how long for delivery", "when will it arrive"],
        "responses": ["We ship to Italy, Europe and worldwide.\n\n- Italy: 2-4 business days\n- Europe: 4-7 business days\n- Worldwide: 7-15 business days\n\nCash on delivery available."]
    },
    {
        "name": "info_warranty",
        "phrases": ["warranty", "is there warranty", "what if it breaks", "returns", "refund"],
        "responses": ["All our machines come with a warranty.\nFor returns and refunds see:\nhttps://www.costycnc.it/politica-di-reso/\n\nFor technical support contact us directly."]
    },
    {
        "name": "info_contacts",
        "phrases": ["how do I contact you", "phone number", "email", "contacts", "where are you"],
        "responses": ["You can contact us through:\n- Website: https://www.costycnc.it\n- Facebook: facebook.com/costelcnc\n- YouTube: youtube.com/@bobyca2003\n- eBay: ebay.it/str/costycnc"]
    },
    {
        "name": "info_tutorials",
        "phrases": ["are there tutorials", "how to use", "video tutorial", "guide", "manual"],
        "responses": ["Yes! Tutorials available at:\n- YouTube: https://www.youtube.com/@bobyca2003\n- Blog: https://costycnc1.blogspot.com/\n- Site tutorials: https://www.costycnc.it/tutorial"]
    },
    {
        "name": "info_purchase",
        "phrases": ["how do I buy", "how to purchase", "where to buy", "can I pay with paypal"],
        "responses": ["You can buy from:\n- eBay: https://www.ebay.it/str/costycnc\n- PayPal from our website\n- Cash on delivery (Italy only)"]
    }
]


# ==========================================
# CREATE GITHUB PROJECT
# ==========================================
def create_readme():
    readme = """# Dialogflow ES - ZIP Import Guide

**Complete guide to import a chatbot into Dialogflow ES**, with the correct
ZIP format, common errors and field-tested solutions.

Born from **3 days of real attempts** with the [CostyCNC](https://www.costycnc.it) project —
every problem we encountered, now documented so nobody else has to hit them.

## Why this guide

The official Dialogflow ES documentation **does not explain** how to build
the ZIP from scratch. The errors it returns are cryptic and don't say what
is wrong. Anyone trying to do this as a beginner spends days on it.

**This guide solves exactly that.**

## What you will find here

- **Exact** format of the importable ZIP
- **10 common problems** with tested solutions
- **Python script** that generates the ZIP automatically
- **Ready example chatbot** (CostyCNC) to start from
- **Step-by-step tutorial** for beginners

## Quick Start

### 1. Generate the ZIP

    python crea_bot.py

Output: `dialogflow-es-chatbot.zip`

### 2. Import into Dialogflow ES

1. Open [dialogflow.cloud.google.com](https://dialogflow.cloud.google.com)
2. Settings -> Export and Import -> **RESTORE FROM ZIP**
3. Upload the ZIP file
4. Type `IMPORT` -> click **IMPORT**

If you see **"Agent import successful"** in green -> DONE!

### 3. Test the bot

In the right panel **"Try it now"**:

    hello
    how do I convert svg to gcode
    how much does it cost

## The 10 problems solved

| # | Problem | Symptom |
|---|---------|---------|
| 1 | Invalid UUID | `'intent-017' is not a valid intent ID` |
| 2 | Wrong filename | `can not be passed into JsonElement` |
| 3 | Malformed JSON | `BadRequestException` |
| 4 | Nested folder | `Nothing to import` |
| 5 | IAM permissions | `Permission 'dialogflow.agents.get' not granted` |
| 6 | Deprecated URL | Old URL `api-client/demo/embedded` |
| 7 | Bot always Fallback | Training phrases not imported |
| 8 | Project missing | Project ID not visible in the list |
| 9 | Nested folder | Script run in wrong folder |
| 10 | IMPORT button grey | Missing confirmation text |

Full details in **[TROUBLESHOOTING.md](TROUBLESHOOTING.md)**

## Correct ZIP format - Golden rules

    dialogflow-es-chatbot.zip
    +-- costycnc-bot/
        +-- agent.json
        +-- package.json
        +-- intents/
            +-- {name}.json
            +-- {name}_usersays_it.json      <- EXACT NAME!

| Rule | Correct | WRONG |
|------|---------|-------|
| Training file name | `{name}_usersays_it.json` | `{name}_user_says.json` |
| Intent ID | UUID v4 | `intent-001` |
| Type field | `"0"` (string) | `0` (number) |
| Encoding | UTF-8 without BOM | UTF-8-BOM |
| Root folder | Only one | `bot/bot/` |

## Project structure

| File | Description |
|------|-------------|
| `crea_bot.py` | Python script that generates the ZIP |
| `TUTORIAL.md` | Step-by-step tutorial |
| `TROUBLESHOOTING.md` | 10 problems + solutions |
| `LICENSE` | MIT |
| `ABOUT.md` | GitHub metadata |

## Who this is for

- **Beginner developers** trying Dialogflow ES for the first time
- **Anyone who has banged their head** against "can not be passed into JsonElement"
- **Anyone who wants to understand** how the Dialogflow ZIP format works
- **Anyone looking for a working chatbot** as a starting point

## Resources

- [Dialogflow ES Docs](https://cloud.google.com/dialogflow/es/docs)
- [Dialogflow Console](https://dialogflow.cloud.google.com)
- [CostyCNC](https://www.costycnc.it)

## License

MIT - see [LICENSE](LICENSE).

## Credits

Born from the real experience of [CostyCNC](https://www.costycnc.it).
If you too have fought with the Dialogflow ZIP format, this repo is for you.
"""
    with open(os.path.join(PROJECT_DIR, "README.md"), "w", encoding="utf-8") as f:
        f.write(readme)
    print("  [OK] README.md")


def create_tutorial():
    tutorial = """# Tutorial: Build a chatbot with Dialogflow ES

Practical guide based on real experience with CostyCNC.

## Before you start

Read **[TROUBLESHOOTING.md](TROUBLESHOOTING.md)**! The Dialogflow ES ZIP
import format has many traps that can block you for days.

## What you need

- Google account (free)
- Access to [dialogflow.cloud.google.com](https://dialogflow.cloud.google.com)
- Python 3.8+ installed
- 30 minutes

## 1. Create the Dialogflow agent

1. Go to [dialogflow.cloud.google.com](https://dialogflow.cloud.google.com)
2. Click **"Create Agent"**
3. Fill in:
   - **Agent name:** `costycnc-bot`
   - **Default Language:** English (en) or Italian (it)
   - **Time Zone:** Europe/Rome
4. Click **CREATE**

After 30 seconds your agent is ready.

**Important:** Note your **Project ID** in Settings -> General.
You will need it later for web integration.

## 2. Understand the ZIP format

Correct structure:

    dialogflow-es-chatbot.zip
    +-- costycnc-bot/
        +-- agent.json
        +-- package.json
        +-- intents/
            +-- {name}.json
            +-- {name}_usersays_it.json

### Golden rules

| Rule | Correct value | WRONG value |
|------|---------------|-------------|
| Training file name | `{name}_usersays_it.json` | `{name}_user_says.json` |
| Intent ID | UUID v4 | `intent-001` |
| Type field | `"0"` (string) | `0` (number) |
| Encoding | UTF-8 without BOM | UTF-8-BOM |

## 3. Generate the ZIP

The `crea_bot.py` script does everything automatically:

    python crea_bot.py

Output: `dialogflow-es-chatbot.zip`

**Run the script from a neutral folder** (e.g. Desktop),
NOT inside a folder already named `costycnc-bot`,
otherwise it creates a **nested folder** inside the ZIP.

## 4. Import into Dialogflow

1. Settings -> **Export and Import**
2. Click **RESTORE FROM ZIP**
3. Upload `dialogflow-es-chatbot.zip`
4. Type `IMPORT` in the text field
5. Click **IMPORT**

If you see **"Agent import successful"** -> DONE!

## 5. Test the bot

1. Right panel -> **"Try it now"**
2. Type: `hello`
3. You should see the bot response

If it replies with Fallback -> see **[TROUBLESHOOTING.md](TROUBLESHOOTING.md)**

## 6. Integrate into your website

### Dialogflow Messenger (recommended)

1. Dialogflow -> **Integrations** -> **Dialogflow Messenger**
2. Click **ENABLE** (if error -> [TROUBLESHOOTING.md](TROUBLESHOOTING.md))
3. Copy the code:

    <script src="https://www.gstatic.com/dialogflow-console/fast/messenger/bootstrap.js?v=1"></script>
    <df-messenger
      intent="WELCOME"
      chat-title="CostyCNC"
      agent-id="YOUR_AGENT_ID"
      language-code="en">
    </df-messenger>

**DO NOT use the old URL** `console.dialogflow.com/api-client/demo/embedded/...`!
It is deprecated.

## 7. Final tips

- Regularly export a backup (Settings -> EXPORT AS ZIP)
- Check the "Training" panel every week
- Add unrecognized phrases to existing intents
- Lower the ML threshold to 0.4 in Settings -> ML Settings
"""
    with open(os.path.join(PROJECT_DIR, "TUTORIAL.md"), "w", encoding="utf-8") as f:
        f.write(tutorial)
    print("  [OK] TUTORIAL.md")


def create_troubleshooting():
    tr = """# Dialogflow ES - Troubleshooting

Every problem we encountered while building a Dialogflow ES chatbot, with
tested solutions.

## Index

1. `'X' is not a valid intent ID. Must be a UUID`
2. `can not be passed into JsonElement`
3. `BadRequestException` during import
4. `Nothing to import` - ZIP not read
5. `Permission 'dialogflow.agents.get' not granted`
6. Old URL `console.dialogflow.com/api-client/demo/embedded` no longer works
7. Bot always replies with Fallback
8. Google Cloud project not showing in the list
9. Nested folder inside the ZIP
10. IMPORT button grey/disabled

---

## 1. `'X' is not a valid intent ID. Must be a UUID`

### Error
    Validate intent with display name 'goodbye' failed because of the following reasons:
    'intent-017' is not a valid intent ID. Must be a UUID.

### Cause
You are using IDs like `intent-001` instead of proper **UUID v4**.

### Solution
Replace:

    "id": f"intent-{counter:03d}",   # WRONG

with:

    import uuid
    "id": str(uuid.uuid4()),         # CORRECT

---

## 2. `can not be passed into JsonElement`

### Error
    This file 'intents/image_to_gcode_user_says.json' can not be passed into JsonElement.
    Check if this is in valid json format.

### Cause
The **training phrases filename** is wrong. Dialogflow ES is extremely
picky about the file name.

### WRONG names
- `image_to_gcode_user_says.json` (singular, no "it")
- `image_to_gcode_usersays.json` (missing "_it")
- `image_to_gcode_user_says_it.json` ("user_says" instead of "usersays")

### CORRECT name

    {intent_name}_usersays_it.json

Correct examples:

    image_to_gcode_usersays_it.json      OK
    svg_to_gcode_usersays_it.json        OK
    confirm_no_usersays_it.json          OK

Must be all attached: **usersays** + **_it**.

---

## 3. `BadRequestException` during import

### Possible causes
- **UTF-8 BOM** at the beginning of the file
- **Apostrophes** not properly handled
- **Emoji** in texts
- JSON with double commas or unbalanced brackets
- File too large (over 10 MB)

### Solution
1. Open with **Notepad++**
2. Menu **Encoding** -> **UTF-8** (NOT "UTF-8 BOM")
3. Save
4. Validate JSON at jsonlint.com

---

## 4. `Nothing to import` - ZIP not read

### Causes
- Nested folder inside the ZIP (e.g. `costycnc-bot/costycnc-bot/`)
- Missing `agent.json` in the root
- Missing `intents/` folder

### Correct structure

    dialogflow-es-chatbot.zip
    +-- costycnc-bot/         <- ONLY ONE folder
        +-- agent.json
        +-- package.json
        +-- intents/
            +-- greeting.json
            +-- greeting_usersays_it.json

### WRONG structure

    dialogflow-es-chatbot.zip
    +-- costycnc-bot/
        +-- costycnc-bot/     <- NESTED!
            +-- agent.json
            +-- intents/

---

## 5. `Permission 'dialogflow.agents.get' not granted`

### Error
    com.google.apps.framework.auth.IamPermissionDeniedException:
    Permission 'dialogflow.agents.get' not granted to cloud-ml-dialogflow-frontend@prod.google.com,
    because no ALLOW or ALLOW_WITH_LOG rule includes that permission.

### Cause
You do not have IAM permissions on the Google Cloud project.
**Or you are working in the WRONG Google Cloud project!**

### Step-by-step solution

**Step 1** - Find the correct Project ID:
Dialogflow -> Settings -> **General** -> copy the **Project ID**

**Step 2** - Go to [Google Cloud Console](https://console.cloud.google.com)

**Step 3** - Top left, select the **correct** project

**Step 4** - Menu -> **IAM & Admin** -> **IAM**

**Step 5** - Find your email address -> click the pencil icon

**Step 6** - Add roles:
- **Dialogflow API Admin**
- **Dialogflow Console Agent Editor**
- **Editor** (generic)

**Step 7** - **SAVE** -> back to Dialogflow -> reload -> retry

---

## 6. Old URL `console.dialogflow.com/api-client/demo/embedded` no longer works

### Error
    The web page at https://console.dialogflow.com/api-client/demo/embedded/...
    might be temporarily down or it may have moved permanently to a new web address.

### Cause
Google has **deprecated** the old "web demo" service.

### Solution - Use Dialogflow Messenger

1. Dialogflow -> **Integrations** -> **Dialogflow Messenger**
2. Click **ENABLE**
3. Copy the code:

    <script src="https://www.gstatic.com/dialogflow-console/fast/messenger/bootstrap.js?v=1"></script>
    <df-messenger
      intent="WELCOME"
      chat-title="CostyCNC"
      agent-id="YOUR_AGENT_ID"
      language-code="en">
    </df-messenger>

**Do NOT confuse `agent-id` with Project ID!**
- `agent-id` = UUID like `9378968c-5941-48e8-95e1-8014f7fa02f5`
- `Project ID` = string like `costycnc-bot-lxxc`

---

## 7. Bot always replies with Fallback

### Causes
- Training phrases **not imported**
- **ML threshold too high** (default 0.7)
- Model needs to **reindex** (1-2 minutes)

### Solution
1. **Verify training phrases:** open the intent -> check the phrases
2. **Click SAVE** in the intent -> forces retraining
3. **Wait 2 minutes**
4. **Retry**
5. If still failing -> **lower ML threshold:**
   Settings -> **ML Settings** -> **Classification threshold** -> `0.4`

---

## 8. Google Cloud project not showing in the list

### Symptom
In the "Select a project" screen I cannot see the `costycnc-bot` project.

### Causes
1. Logged in with a **different Google account**
2. Project in a **corporate organization** not accessible
3. Dialogflow agent is a **trial/temporary** without a Cloud project
4. Project name is **completely different** (e.g. "My First Project")

### Solution

**Check 1** - Verify the account is the same in Dialogflow and Cloud Console

**Check 2** - Find the real Project ID:
Dialogflow -> Settings -> **General** -> copy the **Project ID**

**Check 3** - Search by ID:
In the "Select project" screen, type the **exact Project ID** in the search field

### If it still does not appear -> Create a new project
1. Google Cloud Console
2. **Select a project** -> **NEW PROJECT**
3. Name: `costycnc-chatbot`
4. Create
5. Back to Dialogflow -> create a new agent selecting this project
6. Reimport the ZIP

---

## 9. Nested folder inside the ZIP

### Cause
You ran the Python script **inside** a folder already named like the agent.

### Solution

    # WRONG: run inside costycnc-bot/
    cd costycnc-bot/
    python crea_bot.py
    # -> creates costycnc-bot/costycnc-bot/

    # CORRECT: run from a neutral folder
    cd /Desktop/work/
    python crea_bot.py
    # -> creates work/costycnc-bot/

---

## 10. IMPORT button grey/disabled

### Cause
You uploaded the ZIP but did not type the confirmation.

### Solution
In the text field type: `IMPORT` (all caps) -> the button becomes clickable.

---

## Final checklist before import

| # | Check | OK? |
|---|-------|-----|
| 1 | All IDs are UUID v4 | [ ] |
| 2 | Training files are named `{name}_usersays_it.json` | [ ] |
| 3 | No file named `_user_says.json` | [ ] |
| 4 | ZIP has only one root folder | [ ] |
| 5 | `agent.json` present | [ ] |
| 6 | Files saved as UTF-8 without BOM | [ ] |
| 7 | JSON validated with jsonlint.com | [ ] |
| 8 | Type field is `"0"` (string) | [ ] |
| 9 | Fields `title`, `textToSpeech`, `condition` present | [ ] |
| 10 | Number of files in `intents/` = 2 x number of intents | [ ] |
"""
    with open(os.path.join(PROJECT_DIR, "TROUBLESHOOTING.md"), "w", encoding="utf-8") as f:
        f.write(tr)
    print("  [OK] TROUBLESHOOTING.md")


def create_about():
    about = """# GitHub Metadata

Values to fill in when creating the repository on GitHub.

## Repository name

    dialogflow-es-zip-import-guide

## Description (short)

    Complete guide to import ZIP into Dialogflow ES: correct format, common errors and tested solutions.

## Description (long - for About)

    Complete guide to import ZIP into Dialogflow ES: correct format,
    common errors and tested solutions. Born from 3 days of real attempts with CostyCNC.

## Website

    https://www.costycnc.it

## Topics (12)

    dialogflow
    dialogflow-es
    dialogflow-tutorial
    chatbot
    import
    troubleshooting
    zip
    python
    uuid
    iam
    costycnc
    english

## How to set up on GitHub

1. Go to your repo page
2. Click the gear icon (settings) next to "About" in the top right
3. Paste the Description
4. Paste the Website
5. Add Topics one by one
6. Save changes

## Social Preview

1. Repository -> Settings -> Social preview
2. Upload image 1280x640px
3. Suggested: error screenshot + title "Dialogflow ES ZIP Import Guide"
"""
    with open(os.path.join(PROJECT_DIR, "ABOUT.md"), "w", encoding="utf-8") as f:
        f.write(about)
    print("  [OK] ABOUT.md")


def create_license():
    lic = """MIT License

Copyright (c) 2026 CostyCNC

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
    with open(os.path.join(PROJECT_DIR, "LICENSE"), "w", encoding="utf-8") as f:
        f.write(lic)
    print("  [OK] LICENSE")


def create_gitignore():
    gi = """# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/

# Generated ZIPs (not uploaded to GitHub)
costycnc-bot/
dialogflow-es-chatbot.zip
*.zip

# OS
.DS_Store
Thumbs.db

# IDE
.vscode/
.idea/
*.swp
"""
    with open(os.path.join(PROJECT_DIR, ".gitignore"), "w", encoding="utf-8") as f:
        f.write(gi)
    print("  [OK] .gitignore")


def create_index_html():
    """Creates the HTML page for manual upload to the website."""
    html = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Dialogflow ES - ZIP Import Guide | CostyCNC</title>

<meta name="description" content="Complete guide to import a chatbot into Dialogflow ES. Correct ZIP format, 10 common problems and tested solutions. Born from real CostyCNC experience.">
<meta name="keywords" content="dialogflow, dialogflow es, chatbot, zip import, troubleshooting, uuid, iam, python, costycnc">
<meta name="author" content="CostyCNC">
<meta name="language" content="en">

<link rel="canonical" href="https://www.costycnc.it/tools/dialogflow-es-zip-import-guide/">
<link rel="alternate" hreflang="it" href="https://www.costycnc.it/tools/dialogflow-es-zip-import-guide/it/">
<link rel="alternate" hreflang="en" href="https://www.costycnc.it/tools/dialogflow-es-zip-import-guide/">
<link rel="alternate" hreflang="x-default" href="https://www.costycnc.it/tools/dialogflow-es-zip-import-guide/">

<style>
  * { box-sizing: border-box; }
  body {
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    line-height: 1.7;
    max-width: 960px;
    margin: 0 auto;
    padding: 40px 20px;
    color: #333;
    background: #fafafa;
  }
  h1 {
    color: #2c3e50;
    border-bottom: 3px solid #4CAF50;
    padding-bottom: 15px;
    font-size: 2em;
  }
  h2 {
    color: #c0392b;
    margin-top: 50px;
    padding: 15px 20px;
    background: #fdecea;
    border-left: 4px solid #dc3545;
    border-radius: 4px;
  }
  h3 { color: #555; margin-top: 30px; }
  p { margin: 15px 0; }
  code {
    background: #f4f4f4;
    padding: 3px 8px;
    border-radius: 4px;
    font-family: "Courier New", monospace;
    color: #c7254e;
    font-size: 0.9em;
  }
  pre {
    background: #2d2d2d;
    color: #f8f8f2;
    padding: 20px;
    border-radius: 8px;
    overflow-x: auto;
    font-size: 0.85em;
    line-height: 1.5;
  }
  pre code {
    background: none;
    color: #f8f8f2;
    padding: 0;
  }
  .intro {
    background: #e8f5e9;
    padding: 20px;
    border-radius: 8px;
    border-left: 4px solid #4CAF50;
    margin: 20px 0;
  }
  .error {
    background: #f8d7da;
    border: 1px solid #f5c6cb;
    color: #721c24;
    padding: 15px;
    border-radius: 6px;
    margin: 15px 0;
    font-family: monospace;
    font-size: 0.9em;
  }
  .error::before {
    content: "ERROR: ";
    font-weight: bold;
  }
  .fix {
    background: #d4edda;
    border: 1px solid #c3e6cb;
    color: #155724;
    padding: 15px;
    border-radius: 6px;
    margin: 15px 0;
  }
  .fix::before {
    content: "SOLUTION: ";
    font-weight: bold;
  }
  .warning {
    background: #fff3cd;
    border: 1px solid #ffeaa7;
    color: #856404;
    padding: 15px;
    border-radius: 6px;
    margin: 20px 0;
  }
  .warning::before {
    content: "WARNING: ";
    font-weight: bold;
  }
  table {
    border-collapse: collapse;
    width: 100%;
    margin: 20px 0;
    background: white;
  }
  th, td {
    border: 1px solid #ddd;
    padding: 12px;
    text-align: left;
  }
  th {
    background: #4CAF50;
    color: white;
  }
  tr:nth-child(even) { background: #f9f9f9; }
  .toc {
    background: white;
    padding: 25px;
    border-radius: 8px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.08);
    margin: 30px 0;
  }
  .toc h3 { margin-top: 0; }
  .toc a {
    display: block;
    padding: 8px 0;
    color: #2196F3;
    text-decoration: none;
    border-bottom: 1px solid #eee;
  }
  .toc a:hover {
    background: #f5f5f5;
    padding-left: 10px;
    transition: 0.2s;
  }
  .badge {
    display: inline-block;
    padding: 3px 10px;
    border-radius: 12px;
    font-size: 0.75em;
    font-weight: bold;
    margin-left: 8px;
    color: white;
  }
  .badge-easy { background: #28a745; }
  .badge-medium { background: #ffc107; color: #333; }
  .badge-hard { background: #dc3545; }
  .cta {
    display: inline-block;
    background: #4CAF50;
    color: white;
    padding: 14px 28px;
    border-radius: 6px;
    text-decoration: none;
    font-weight: bold;
    margin: 10px 5px;
    font-size: 1.05em;
  }
  .cta:hover { background: #45a049; }
  .cta-secondary { background: #2196F3; }
  .cta-secondary:hover { background: #1976D2; }
  footer {
    margin-top: 60px;
    padding-top: 30px;
    border-top: 2px solid #ddd;
    text-align: center;
    color: #666;
    font-size: 0.9em;
  }
  @media (max-width: 600px) {
    body { padding: 20px 15px; }
    h1 { font-size: 1.5em; }
    pre { font-size: 0.75em; padding: 15px; }
  }
</style>
</head>
<body>

<h1>Dialogflow ES - ZIP Import Guide</h1>

<div class="intro">
  <strong>Complete guide to import a chatbot into Dialogflow ES.</strong>
  The correct ZIP format, 10 common problems and field-tested solutions.
  <br><br>
  Born from <strong>3 days of real attempts</strong> with the
  <a href="https://www.costycnc.it">CostyCNC</a> project. Every problem we
  encountered, now documented so nobody else has to hit them.
</div>

<h2>Why this guide exists</h2>

<p>
  The official Dialogflow ES documentation <strong>does not explain</strong>
  how to build the importable ZIP from scratch. The errors it returns are
  cryptic and don't tell you what is actually wrong. As a beginner you can
  spend days stuck on the same error.
</p>

<p>
  <strong>This guide solves exactly that.</strong>
</p>

<h2>What you will find here</h2>

<ul>
  <li>The <strong>exact format</strong> of the importable ZIP</li>
  <li><strong>10 common problems</strong> with tested solutions</li>
  <li>A <strong>Python script</strong> that generates the ZIP automatically</li>
  <li>A <strong>ready example chatbot</strong> (CostyCNC) to start from</li>
  <li>A <strong>step-by-step tutorial</strong> for beginners</li>
</ul>

<h2>Quick Start</h2>

<h3>1. Generate the ZIP</h3>
<pre><code>python crea_bot.py</code></pre>
<p>Output: <code>dialogflow-es-chatbot.zip</code></p>

<h3>2. Import into Dialogflow ES</h3>
<ol>
  <li>Open <a href="https://dialogflow.cloud.google.com" target="_blank">dialogflow.cloud.google.com</a></li>
  <li>Settings &rarr; Export and Import &rarr; <strong>RESTORE FROM ZIP</strong></li>
  <li>Upload the ZIP file</li>
  <li>Type <code>IMPORT</code> &rarr; click <strong>IMPORT</strong></li>
</ol>

<p>If you see <strong>"Agent import successful"</strong> in green &rarr; DONE!</p>

<h3>3. Test the bot</h3>
<p>In the right panel <strong>"Try it now"</strong>:</p>
<pre><code>hello
how do I convert svg to gcode
how much does it cost</code></pre>

<div class="toc">
  <h3>The 10 problems solved</h3>
  <a href="#p1">1. <code>'X' is not a valid intent ID. Must be a UUID</code> <span class="badge badge-easy">EASY</span></a>
  <a href="#p2">2. <code>can not be passed into JsonElement</code> <span class="badge badge-medium">MEDIUM</span></a>
  <a href="#p3">3. <code>BadRequestException</code> during import <span class="badge badge-medium">MEDIUM</span></a>
  <a href="#p4">4. <code>Nothing to import</code> - ZIP not read <span class="badge badge-easy">EASY</span></a>
  <a href="#p5">5. <code>Permission 'dialogflow.agents.get' not granted</code> <span class="badge badge-hard">HARD</span></a>
  <a href="#p6">6. Old URL <code>console.dialogflow.com/api-client/demo/embedded</code> no longer works <span class="badge badge-easy">EASY</span></a>
  <a href="#p7">7. Bot always replies with Fallback <span class="badge badge-medium">MEDIUM</span></a>
  <a href="#p8">8. Google Cloud project not showing in the list <span class="badge badge-hard">HARD</span></a>
  <a href="#p9">9. Nested folder inside the ZIP <span class="badge badge-easy">EASY</span></a>
  <a href="#p10">10. IMPORT button grey/disabled <span class="badge badge-easy">EASY</span></a>
</div>

<h2 id="p1">Problem 1: <code>'X' is not a valid intent ID. Must be a UUID</code> <span class="badge badge-easy">EASY</span></h2>

<div class="error">
Validate intent with display name 'goodbye' failed because of the following reasons: 'intent-017' is not a valid intent ID. Must be a UUID.
</div>

<h3>Cause</h3>
<p>You are using IDs like <code>intent-001</code> instead of proper <strong>UUID v4</strong>.</p>

<h3>Solution</h3>
<p>Replace:</p>
<pre><code>"id": f"intent-{counter:03d}",   # WRONG</code></pre>
<p>with:</p>
<pre><code>import uuid
"id": str(uuid.uuid4()),         # CORRECT</code></pre>

<div class="fix">
Every <code>id</code> (intent, training phrase, response) must be generated with <code>str(uuid.uuid4())</code>.
</div>

<h2 id="p2">Problem 2: <code>can not be passed into JsonElement</code> <span class="badge badge-medium">MEDIUM</span></h2>

<div class="error">
This file 'intents/image_to_gcode_user_says.json' can not be passed into JsonElement. Check if this is in valid json format.
</div>

<h3>Cause</h3>
<p>The <strong>training phrases filename</strong> is wrong. Dialogflow ES is extremely picky about it.</p>

<h3>WRONG names</h3>
<table>
  <tr><th>Filename</th><th>Why it's wrong</th></tr>
  <tr><td><code>image_to_gcode_user_says.json</code></td><td>"user_says" (singular, no "it")</td></tr>
  <tr><td><code>image_to_gcode_usersays.json</code></td><td>Missing "_it" suffix</td></tr>
  <tr><td><code>image_to_gcode_user_says_it.json</code></td><td>"user_says" instead of "usersays"</td></tr>
</table>

<h3>CORRECT name</h3>
<pre><code>{intent_name}_usersays_it.json</code></pre>

<div class="fix">
Must be all attached: <strong>usersays</strong> (plural, no underscore) + <strong>_it</strong> (language).
</div>

<h2 id="p3">Problem 3: <code>BadRequestException</code> during import <span class="badge badge-medium">MEDIUM</span></h2>

<div class="error">
com.google.apps.framework.request.BadRequestException
</div>

<h3>Possible causes</h3>
<ul>
  <li><strong>UTF-8 BOM</strong> at the beginning of the file (invisible character)</li>
  <li><strong>Apostrophes</strong> not properly handled</li>
  <li><strong>Emoji</strong> in texts</li>
  <li>JSON with double commas or unbalanced brackets</li>
  <li>File too large (over 10 MB)</li>
</ul>

<h3>Solution</h3>
<ol>
  <li>Open the file with <strong>Notepad++</strong></li>
  <li>Menu <strong>Encoding</strong> &rarr; <strong>UTF-8</strong> (NOT "UTF-8 BOM")</li>
  <li>Save</li>
  <li>Validate JSON at <a href="https://jsonlint.com" target="_blank">jsonlint.com</a></li>
</ol>

<div class="fix">
Always save files as <strong>UTF-8 without BOM</strong>.
</div>

<h2 id="p4">Problem 4: <code>Nothing to import</code> <span class="badge badge-easy">EASY</span></h2>

<h3>Causes</h3>
<ul>
  <li>Nested folder inside the ZIP (e.g. <code>costycnc-bot/costycnc-bot/</code>)</li>
  <li>Missing <code>agent.json</code> in the root</li>
  <li>Missing <code>intents/</code> folder</li>
</ul>

<h3>Correct structure</h3>
<pre><code>dialogflow-es-chatbot.zip
+-- costycnc-bot/         &lt;- ONLY ONE folder
    +-- agent.json
    +-- package.json
    +-- intents/
        +-- greeting.json
        +-- greeting_usersays_it.json</code></pre>

<h3>WRONG structure</h3>
<pre><code>dialogflow-es-chatbot.zip
+-- costycnc-bot/
    +-- costycnc-bot/     &lt;- NESTED!
        +-- agent.json
        +-- intents/</code></pre>

<div class="fix">
Zip <strong>the folder</strong>, not its content. The result must have <code>agent.json</code> in a subfolder, not in the ZIP root.
</div>

<h2 id="p5">Problem 5: <code>Permission 'dialogflow.agents.get' not granted</code> <span class="badge badge-hard">HARD</span></h2>

<div class="error">
com.google.apps.framework.auth.IamPermissionDeniedException: Permission 'dialogflow.agents.get' not granted to cloud-ml-dialogflow-frontend@prod.google.com, because no ALLOW or ALLOW_WITH_LOG rule includes that permission.
</div>

<h3>Cause</h3>
<p>
  You are trying to enable an integration (e.g. Dialogflow Messenger) but
  your account <strong>does not have the necessary IAM permissions</strong>
  on the Google Cloud project.
</p>
<p>
  <strong>OR you are working in the WRONG Google Cloud project!</strong>
  This is the most common cause.
</p>

<h3>Step-by-step solution</h3>

<p><strong>Step 1</strong> - Find the correct Project ID:<br>
Dialogflow &rarr; Settings &rarr; <strong>General</strong> &rarr; copy the <strong>Project ID</strong></p>

<p><strong>Step 2</strong> - Go to <a href="https://console.cloud.google.com" target="_blank">Google Cloud Console</a></p>

<p><strong>Step 3</strong> - Top left, click the project name and <strong>select the correct project</strong>.
<br>If it does not appear &rarr; see <a href="#p8">Problem 8</a></p>

<p><strong>Step 4</strong> - Menu &rarr; <strong>IAM &amp; Admin</strong> &rarr; <strong>IAM</strong></p>

<p><strong>Step 5</strong> - Find your <strong>email address</strong> in the list &rarr; click the pencil icon</p>

<p><strong>Step 6</strong> - Add roles:
<ul>
  <li><strong>Dialogflow API Admin</strong></li>
  <li><strong>Dialogflow Console Agent Editor</strong></li>
  <li><strong>Editor</strong> (generic)</li>
</ul>
</p>

<p><strong>Step 7</strong> - <strong>SAVE</strong> &rarr; back to Dialogflow &rarr; reload &rarr; retry</p>

<div class="fix">
After adding IAM permissions, the <strong>ENABLE</strong> button becomes clickable.
</div>

<h2 id="p6">Problem 6: Old URL <code>console.dialogflow.com/api-client/demo/embedded</code> no longer works <span class="badge badge-easy">EASY</span></h2>

<div class="error">
The web page at https://console.dialogflow.com/api-client/demo/embedded/... might be temporarily down or it may have moved permanently to a new web address.
</div>

<h3>Cause</h3>
<p>Google has <strong>deprecated</strong> the old "web demo" service.</p>

<h3>Solution - Use Dialogflow Messenger</h3>

<p><strong>Step 1</strong> - Dialogflow &rarr; <strong>Integrations</strong> &rarr; <strong>Dialogflow Messenger</strong></p>
<p><strong>Step 2</strong> - Click <strong>ENABLE</strong> (if error &rarr; <a href="#p5">Problem 5</a>)</p>
<p><strong>Step 3</strong> - Copy the generated code:</p>

<pre><code>&lt;script src="https://www.gstatic.com/dialogflow-console/fast/messenger/bootstrap.js?v=1"&gt;&lt;/script&gt;
&lt;df-messenger
  intent="WELCOME"
  chat-title="CostyCNC"
  agent-id="YOUR_AGENT_ID"
  language-code="en"&gt;
&lt;/df-messenger&gt;</code></pre>

<div class="warning">
<strong>Do NOT confuse <code>agent-id</code> with Project ID!</strong><br>
- <code>agent-id</code> = UUID like <code>9378968c-5941-48e8-95e1-8014f7fa02f5</code><br>
- <code>Project ID</code> = string like <code>costycnc-bot-lxxc</code>
</div>

<h2 id="p7">Problem 7: Bot always replies with Fallback <span class="badge badge-medium">MEDIUM</span></h2>

<h3>Possible causes</h3>
<ul>
  <li>Training phrases <strong>not imported</strong></li>
  <li><strong>ML threshold too high</strong> (default 0.7)</li>
  <li>Model needs to <strong>reindex</strong> (1-2 minutes)</li>
</ul>

<h3>Solution</h3>
<ol>
  <li><strong>Verify training phrases:</strong> open the intent &rarr; check the phrases</li>
  <li><strong>Click SAVE</strong> in the intent &rarr; forces retraining</li>
  <li><strong>Wait 2 minutes</strong></li>
  <li><strong>Retry</strong></li>
  <li>If still failing &rarr; <strong>lower ML threshold:</strong></li>
</ol>

<p>Settings &rarr; <strong>ML Settings</strong> &rarr; <strong>Classification threshold</strong>: change from <code>0.7</code> to <code>0.4</code></p>

<h2 id="p8">Problem 8: Google Cloud project not showing in the list <span class="badge badge-hard">HARD</span></h2>

<h3>Symptom</h3>
<p>In the "Select a project" screen I cannot see the <code>costycnc-bot</code> project.</p>

<h3>Possible causes</h3>
<ol>
  <li>Logged in with a <strong>different Google account</strong></li>
  <li>Project in a <strong>corporate organization</strong> not accessible</li>
  <li>Dialogflow agent is a <strong>trial/temporary</strong> without a Cloud project</li>
  <li>Project name is <strong>completely different</strong> (e.g. "My First Project")</li>
</ol>

<h3>Solution</h3>

<p><strong>Check 1</strong> - Verify the account is the same in Dialogflow and Cloud Console</p>
<p><strong>Check 2</strong> - Find the real Project ID: Dialogflow &rarr; Settings &rarr; <strong>General</strong></p>
<p><strong>Check 3</strong> - Search by ID in the "Select project" screen</p>

<div class="fix">
If the project <strong>really exists</strong>, it will appear when searching by ID even if the name is different.<br>
If it <strong>does not appear</strong>, the agent is probably a temporary trial &rarr; you need to create a new agent in a real Cloud project.
</div>

<h3>Alternative - Create a new project</h3>
<ol>
  <li>Go to <a href="https://console.cloud.google.com" target="_blank">Google Cloud Console</a></li>
  <li>Top &rarr; <strong>Select a project</strong> &rarr; <strong>NEW PROJECT</strong></li>
  <li>Name: <code>costycnc-chatbot</code></li>
  <li>Create</li>
  <li>Back to Dialogflow &rarr; create a new agent selecting this project</li>
  <li>Reimport the ZIP</li>
</ol>

<h2 id="p9">Problem 9: Nested folder inside the ZIP <span class="badge badge-easy">EASY</span></h2>

<h3>Cause</h3>
<p>
  You ran the Python script <strong>inside</strong> a folder that is already
  named like the agent (e.g. <code>costycnc-bot</code>). The script creates
  the folder <code>costycnc-bot</code> &rarr; result: <code>costycnc-bot/costycnc-bot/</code>.
</p>

<h3>Solution</h3>
<pre><code># WRONG: run inside costycnc-bot/
cd costycnc-bot/
python crea_bot.py
# -> creates costycnc-bot/costycnc-bot/

# CORRECT: run from a neutral folder
cd /Desktop/work/
python crea_bot.py
# -> creates work/costycnc-bot/</code></pre>

<div class="fix">
Always run the script from a <strong>neutral folder</strong> that is <strong>not named like the agent</strong>.
</div>

<h2 id="p10">Problem 10: IMPORT button grey/disabled <span class="badge badge-easy">EASY</span></h2>

<h3>Cause</h3>
<p>You uploaded the ZIP but did not <strong>type the confirmation</strong>. Dialogflow requires you to type the word <code>IMPORT</code> to activate the button (prevents accidental clicks).</p>

<h3>Solution</h3>
<ol>
  <li>In the text field type: <code>IMPORT</code> (all caps)</li>
  <li>The <strong>IMPORT</strong> button becomes blue/clickable</li>
  <li>Click it</li>
</ol>

<div class="fix">
Type exactly <strong>IMPORT</strong> - no spaces, no lowercase.
</div>

<h2>Final checklist before import</h2>

<table>
  <tr><th>#</th><th>Check</th><th>OK?</th></tr>
  <tr><td>1</td><td>All IDs are UUID v4</td><td>[ ]</td></tr>
  <tr><td>2</td><td>Training files named <code>{name}_usersays_it.json</code></td><td>[ ]</td></tr>
  <tr><td>3</td><td>No file named <code>_user_says.json</code> (without "it")</td><td>[ ]</td></tr>
  <tr><td>4</td><td>ZIP has <strong>only one</strong> root folder</td><td>[ ]</td></tr>
  <tr><td>5</td><td><code>agent.json</code> present in the folder</td><td>[ ]</td></tr>
  <tr><td>6</td><td>Files saved as <strong>UTF-8 without BOM</strong></td><td>[ ]</td></tr>
  <tr><td>7</td><td>JSON validated at <a href="https://jsonlint.com" target="_blank">jsonlint.com</a></td><td>[ ]</td></tr>
  <tr><td>8</td><td><code>type</code> field is <code>"0"</code> (string)</td><td>[ ]</td></tr>
  <tr><td>9</td><td><code>title</code>, <code>textToSpeech</code>, <code>condition</code> fields present</td><td>[ ]</td></tr>
  <tr><td>10</td><td>Number of files in <code>intents/</code> = 2 x number of intents</td><td>[ ]</td></tr>
</table>

<h2>Need more help?</h2>

<p>
  <a href="https://github.com/YOUR_USERNAME/dialogflow-es-zip-import-guide" class="cta" target="_blank">
    View on GitHub
  </a>
  <a href="https://www.costycnc.it" class="cta cta-secondary">
    CostyCNC website
  </a>
</p>

<footer>
  <p>
    <strong>Dialogflow ES ZIP Import Guide</strong><br>
    Born from real experience with <a href="https://www.costycnc.it">CostyCNC</a>.<br>
    Licensed under MIT. Free for personal and commercial use.
  </p>
  <p>Last updated: 2026</p>
</footer>

</body>
</html>
"""
    with open(os.path.join(PROJECT_DIR, "index.html"), "w", encoding="utf-8") as f:
        f.write(html)
    print("  [OK] index.html")


def create_github_project():
    if os.path.exists(PROJECT_DIR):
        shutil.rmtree(PROJECT_DIR)
    os.makedirs(PROJECT_DIR)
    
    print("[1/2] Creating GitHub project folder...")
    create_readme()
    create_tutorial()
    create_troubleshooting()
    create_about()
    create_license()
    create_gitignore()
    create_index_html()
    
    # Copy crea_bot.py to project
    script_path = os.path.abspath(__file__)
    if os.path.exists(script_path):
        shutil.copy(script_path, os.path.join(PROJECT_DIR, "crea_bot.py"))
        print("  [OK] crea_bot.py")


# ==========================================
# CREATE DIALOGFLOW BOT (IMPORTABLE ZIP)
# ==========================================
def create_dialogflow_zip():
    if os.path.exists(AGENT_NAME):
        shutil.rmtree(AGENT_NAME)
    
    os.makedirs(os.path.join(AGENT_NAME, "intents"))
    
    agent = {
        "id": str(uuid.uuid4()),
        "description": "CostyCNC virtual assistant",
        "language": "it",
        "shortDescription": "CNC foam cutter support bot",
        "linkToDocs": "https://www.costycnc.it",
        "disableInteractionLogs": False,
        "disableStackdriverLogs": True,
        "defaultTimezone": "Europe/Rome",
        "webhook": {
            "available": False,
            "useForDomains": False,
            "cloudFunctionsEnabled": False,
            "cloudFunctionsInitialized": False
        },
        "isPrivate": True,
        "mlMinConfidence": 0.4,
        "onePlatformApiVersion": "v2"
    }
    with open(os.path.join(AGENT_NAME, "agent.json"), "w", encoding="utf-8") as f:
        json.dump(agent, f, ensure_ascii=False, indent=2)
    
    with open(os.path.join(AGENT_NAME, "package.json"), "w") as f:
        json.dump({"version": "1.0.0"}, f)
    
    for intent in intents:
        # File 1: intent definition
        intent_data = {
            "id": str(uuid.uuid4()),
            "name": intent["name"],
            "auto": True,
            "contexts": [],
            "responses": [{
                "resetContexts": False,
                "action": "",
                "affectedContexts": [],
                "parameters": [],
                "messages": [{
                    "type": "0",
                    "title": "",
                    "textToSpeech": "",
                    "lang": "en",
                    "speech": intent["responses"],
                    "condition": ""
                }],
                "speech": []
            }],
            "priority": 500000,
            "webhookUsed": False,
            "webhookForSlotFilling": False,
            "fallbackIntent": False,
            "events": [],
            "conditionalResponses": [],
            "condition": "",
            "conditionalFollowupEvents": []
        }
        with open(os.path.join(AGENT_NAME, "intents", intent["name"] + ".json"), "w", encoding="utf-8") as f:
            json.dump(intent_data, f, ensure_ascii=False, indent=2)
        
        # File 2: training phrases (_usersays_it.json - EXACT NAME!)
        usersays = [{
            "id": str(uuid.uuid4()),
            "data": [{"text": phrase, "userDefined": False}],
            "isTemplate": False,
            "count": 0,
            "lang": "en",
            "updated": 0
        } for phrase in intent["phrases"]]
        
        usersays_filename = intent["name"] + "_usersays_it.json"
        with open(os.path.join(AGENT_NAME, "intents", usersays_filename), "w", encoding="utf-8") as f:
            json.dump(usersays, f, ensure_ascii=False, indent=2)
    
    # Create ZIP
    if os.path.exists(ZIP_NAME):
        os.remove(ZIP_NAME)
    with zipfile.ZipFile(ZIP_NAME, "w", zipfile.ZIP_DEFLATED) as z:
        for root, dirs, files in os.walk(AGENT_NAME):
            for file in files:
                fp = os.path.join(root, file)
                z.write(fp, os.path.relpath(fp, "."))
    
    print("[2/2] Dialogflow ZIP created: " + ZIP_NAME)
    print("      Contains " + str(len(intents)) + " intents (" + str(len(intents)*2) + " files total)")


# ==========================================
# MAIN
# ==========================================
if __name__ == "__main__":
    print("=" * 60)
    print("GITHUB PROJECT GENERATOR")
    print("Dialogflow ES - ZIP Import Guide")
    print("=" * 60)
    print()
    
    create_github_project()
    print()
    create_dialogflow_zip()
    print()
    
    print("=" * 60)
    print("COMPLETED!")
    print("=" * 60)
    print()
    print("Project folder:     " + PROJECT_DIR + "/")
    print("Dialogflow ZIP:     " + ZIP_NAME)
    print()
    print("Next steps:")
    print("  1. Go to https://github.com/new")
    print("  2. Repository name: " + PROJECT_DIR)
    print("  3. Description: Complete guide to import ZIP into Dialogflow ES")
    print("  4. Public, no README/gitignore/license")
    print("  5. Upload files from " + PROJECT_DIR + "/")
    print("  6. Add Topics (see ABOUT.md)")
    print()
    print("For manual website upload:")
    print("  Upload index.html to your web server")
    print("  It is a standalone HTML page (no dependencies)")
