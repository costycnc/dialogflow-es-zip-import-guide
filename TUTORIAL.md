# Tutorial: Build a chatbot with Dialogflow ES

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
