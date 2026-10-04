# Dialogflow ES - ZIP Import Guide

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
