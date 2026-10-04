    readme = """# Dialogflow ES - Guida all'import ZIP (problemi risolti)

**Guida completa per importare un chatbot in Dialogflow ES**, con il formato
ZIP corretto, gli errori comuni e le soluzioni testate sul campo.

Nasce da **3 giorni di tentativi reali** con il progetto [CostyCNC](https://www.costycnc.it) —
tutti i problemi che abbiamo incontrato, ora documentati per non farli
incontrare a nessun altro.

## Perche questa guida

La documentazione ufficiale di Dialogflow ES **non spiega** come costruire
lo ZIP da zero. Gli errori che restituisce sono criptici e non dicono cosa
e sbagliato. Chiunque provi a farlo da principiante ci mette giorni.

**Questa guida risolve esattamente questo.**

## Cosa trovi qui

- Formato **esatto** dello ZIP importabile
- **10 problemi comuni** con soluzioni testate
- **Script Python** che genera lo ZIP automaticamente
- **Chatbot esempio** pronto (CostyCNC) da cui partire
- **Tutorial** passo-passo per principianti

## Quick Start

### 1. Genera lo ZIP

    python crea_bot.py

Output: `dialogflow-es-chatbot.zip`

### 2. Importa in Dialogflow ES

1. Apri [dialogflow.cloud.google.com](https://dialogflow.cloud.google.com)
2. Settings -> Export and Import -> **RESTORE FROM ZIP**
3. Carica il file ZIP
4. Digita `IMPORT` -> clicca **IMPORT**

Se vedi **"Agent import successful"** in verde -> FATTO!

### 3. Testa il bot

Nel pannello destro **"Try it now"**:

    ciao
    come converto svg in gcode
    quanto costa

## I 10 problemi risolti

| # | Problema | Sintomo |
|---|----------|---------|
| 1 | UUID non valido | `'intent-017' is not a valid intent ID` |
| 2 | Nome file sbagliato | `can not be passed into JsonElement` |
| 3 | JSON malformato | `BadRequestException` |
| 4 | Cartella doppia | `Nothing to import` |
| 5 | Permessi IAM | `Permission 'dialogflow.agents.get' not granted` |
| 6 | URL dismesso | Vecchio `console.dialogflow.com/api-client/demo/embedded` |
| 7 | Bot risponde Fallback | Training phrases non importate |
| 8 | Progetto mancante | Project ID non visibile nella lista |
| 9 | Cartella doppia | Script eseguito in cartella sbagliata |
| 10 | IMPORT grigio | Manca digitazione conferma |

Dettagli completi in **[TROUBLESHOOTING.md](TROUBLESHOOTING.md)**

## Formato ZIP corretto - Regole d'oro

    dialogflow-es-chatbot.zip
    +-- costycnc-bot/
        +-- agent.json
        +-- package.json
        +-- intents/
            +-- {name}.json
            +-- {name}_usersays_it.json      <- NOME ESATTO!

| Regola | Corretto | SBAGLIATO |
|--------|----------|-----------|
| Nome file training | `{name}_usersays_it.json` | `{name}_user_says.json` |
| ID intent | UUID v4 | `intent-001` |
| Campo type | `"0"` (stringa) | `0` (numero) |
| Encoding | UTF-8 senza BOM | UTF-8-BOM |
| Cartella radice | Una sola | `bot/bot/` |

## Struttura del progetto

| File | Descrizione |
|------|-------------|
| `crea_bot.py` | Script Python che genera lo ZIP |
| `TUTORIAL.md` | Tutorial passo-passo |
| `TROUBLESHOOTING.md` | 10 problemi + soluzioni |
| `LICENSE` | MIT |
| `ABOUT.md` | Metadati per GitHub |

## A chi serve

- **Sviluppatori principianti** che provano Dialogflow ES per la prima volta
- **Chi ha sbattuto la testa** contro l'errore "can not be passed into JsonElement"
- **Chi vuole capire** come funziona il formato ZIP di Dialogflow
- **Chi cerca un chatbot funzionante** da cui partire

## Risorse

- [Dialogflow ES Docs](https://cloud.google.com/dialogflow/es/docs)
- [Dialogflow Console](https://dialogflow.cloud.google.com)
- [CostyCNC](https://www.costycnc.it)

## Licenza

MIT - vedi [LICENSE](LICENSE).

## Crediti

Nato dall'esperienza reale di [CostyCNC](https://www.costycnc.it).
Se anche tu hai combattuto con il formato ZIP di Dialogflow, questo repo e per te.
"""
