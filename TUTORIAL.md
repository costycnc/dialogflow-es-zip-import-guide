# Tutorial: Crea un chatbot con Dialogflow ES

Guida pratica basata sull'esperienza reale con CostyCNC.

## Prima di iniziare

Leggi **[TROUBLESHOOTING.md](TROUBLESHOOTING.md)**! Il formato di importazione
ZIP di Dialogflow ES ha molte trappole che possono bloccarti per giorni.

## Cosa ti serve

- Account Google (gratis)
- Accesso a [dialogflow.cloud.google.com](https://dialogflow.cloud.google.com)
- Python 3.8+ installato
- 30 minuti

## 1. Creare l'agent Dialogflow

1. Vai su [dialogflow.cloud.google.com](https://dialogflow.cloud.google.com)
2. Clicca **"Create Agent"**
3. Compila:
   - **Agent name:** `costycnc-bot`
   - **Default Language:** Italian (it)
   - **Time Zone:** Europe/Rome
4. Clicca **CREATE**

Dopo 30 secondi hai il tuo agent.

**Importante:** Prendi nota del **Project ID** in Settings -> General.
Ti servira dopo per l'integrazione web.

## 2. Capire il formato ZIP

Struttura corretta:

    costycnc-bot.zip
    +-- costycnc-bot/
        +-- agent.json
        +-- package.json
        +-- intents/
            +-- {name}.json
            +-- {name}_usersays_it.json

### Regole d'oro

| Regola | Valore corretto | Valore SBAGLIATO |
|--------|----------------|------------------|
| Nome file training | `{name}_usersays_it.json` | `{name}_user_says.json` |
| ID intent | UUID v4 | `intent-001` |
| Campo `type` | `"0"` (stringa) | `0` (numero) |
| Encoding | UTF-8 senza BOM | UTF-8-BOM |

## 3. Generare lo ZIP

Lo script `crea_bot.py` fa tutto automaticamente:

    python crea_bot.py

Output: `costycnc-bot.zip`

**Esegui lo script da una cartella neutra** (es. Desktop),
NON dentro una cartella che si chiama gia `costycnc-bot`,
altrimenti crea una **cartella doppia** dentro lo ZIP.

## 4. Importare in Dialogflow

1. Settings -> **Export and Import**
2. Clicca **RESTORE FROM ZIP**
3. Carica `costycnc-bot.zip`
4. Digita `IMPORT` nel campo di testo
5. Clicca **IMPORT**

Se vedi **"Agent import successful"** -> HAI FATTO!

## 5. Testare il bot

1. Pannello destro -> **"Try it now"**
2. Scrivi: `ciao`
3. Dovresti vedere la risposta del bot

Se risponde col Fallback -> vedi **[TROUBLESHOOTING.md](TROUBLESHOOTING.md)**

## 6. Integrare nel sito

### Dialogflow Messenger (raccomandato)

1. Dialogflow -> **Integrations** -> **Dialogflow Messenger**
2. Clicca **ENABLE** (se da errore -> [TROUBLESHOOTING.md](TROUBLESHOOTING.md))
3. Copia il codice:

    <script src="https://www.gstatic.com/dialogflow-console/fast/messenger/bootstrap.js?v=1"></script>
    <df-messenger
      intent="WELCOME"
      chat-title="CostyCNC"
      agent-id="IL_TUO_AGENT_ID"
      language-code="it">
    </df-messenger>

**NON usare il vecchio URL** `console.dialogflow.com/api-client/demo/embedded/...`!
E dismesso.

## 7. Consigli finali

- Esporta regolarmente un backup (Settings -> EXPORT AS ZIP)
- Controlla il pannello "Training" ogni settimana
- Aggiungi le frasi non riconosciute alle intent esistenti
- Abbassa la soglia ML a 0.4 in Settings -> ML Settings
