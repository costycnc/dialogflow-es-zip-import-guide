# Dialogflow ES - Troubleshooting

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
