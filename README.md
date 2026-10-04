# CostyCNC Chatbot - Dialogflow ES

Chatbot di assistenza per [CostyCNC](https://www.costycnc.it) costruito con **Dialogflow ES**.

## ATTENZIONE - Leggi prima questo

Questo repository nasce da **mesi di tentativi ed errori** con Dialogflow ES.
Il formato di importazione ZIP **non e documentato ufficialmente** e ci sono
molte "trappole" che possono bloccarti per giorni.

Se stai cercando di importare un bot in Dialogflow ES e ti da errore,
leggi prima **[TROUBLESHOOTING.md](TROUBLESHOOTING.md)**.

## Quick Start

### Prerequisiti
- Python 3.8+
- Account Google
- 30 minuti

### 1. Genera lo ZIP importabile

    python crea_bot.py

Output: `costycnc-bot.zip`

### 2. Importa in Dialogflow

1. Apri [dialogflow.cloud.google.com](https://dialogflow.cloud.google.com)
2. Crea un nuovo agent (o apri il tuo)
3. Settings -> Export and Import -> **RESTORE FROM ZIP**
4. Carica `costycnc-bot.zip`
5. Digita `IMPORT` -> clicca **IMPORT**

Se vedi **"Agent import successful"** in verde -> FATTO!

### 3. Testa

Nel pannello destro **"Try it now"**:

    ciao
    come converto svg in gcode
    quanto costa
    firmware

### 4. Integra nel sito

Vedi **[TUTORIAL.md](TUTORIAL.md)** -> sezione "Integrazione web"

## Struttura progetto

| File | Descrizione |
|------|-------------|
| `crea_bot.py` | Script Python che genera lo ZIP |
| `TUTORIAL.md` | Tutorial passo-passo per principianti |
| `TROUBLESHOOTING.md` | 10 problemi comuni e soluzioni |
| `LICENSE` | Licenza MIT |

## Problemi comuni (sintesi)

| Errore | Soluzione |
|--------|-----------|
| `'X' is not a valid intent ID. Must be a UUID` | Usa `str(uuid.uuid4())` |
| `can not be passed into JsonElement` | Nome file deve essere `{name}_usersays_it.json` |
| `BadRequestException` | JSON malformato o BOM presente |
| `Nothing to import` | Cartella doppia o manca `agent.json` |
| `Permission 'dialogflow.agents.get' not granted` | Progetto Google Cloud sbagliato |
| URL `console.dialogflow.com/api-client/demo/embedded/...` non funziona | URL dismesso, usa Dialogflow Messenger |

Vedi **[TROUBLESHOOTING.md](TROUBLESHOOTING.md)** per i dettagli.

## Formato ZIP di Dialogflow ES - Regole d'oro

    costycnc-bot.zip
    +-- costycnc-bot/
        +-- agent.json
        +-- package.json
        +-- intents/
            +-- {name}.json
            +-- {name}_usersays_it.json

| Regola | Corretto | SBAGLIATO |
|--------|----------|-----------|
| Nome file training | `{name}_usersays_it.json` | `{name}_user_says.json` |
| ID intent | UUID v4 | `intent-001` |
| Campo `type` | `"0"` (stringa) | `0` (numero) |
| Encoding | UTF-8 senza BOM | UTF-8-BOM |
| Cartella doppia | Mai | `bot/bot/` |

## Integrazione web

**Requisito:** Devi avere un **progetto Google Cloud** collegato all'agent.

    <script src="https://www.gstatic.com/dialogflow-console/fast/messenger/bootstrap.js?v=1"></script>
    <df-messenger
      intent="WELCOME"
      chat-title="CostyCNC"
      agent-id="IL_TUO_AGENT_ID"
      language-code="it">
    </df-messenger>

ATTENZIONE: `agent-id` **NON e il Project ID**! E un UUID tipo `9378968c-5941-48e8-95e1-8014f7fa02f5`.

## Risorse

- [Dialogflow ES Docs](https://cloud.google.com/dialogflow/es/docs)
- [Dialogflow Console](https://dialogflow.cloud.google.com)
- [CostyCNC](https://www.costycnc.it)

## Licenza

MIT - vedi [LICENSE](LICENSE).

## Crediti

Creato con l'esperienza reale di [CostyCNC](https://www.costycnc.it).

---

**Nota:** Dialogflow ES e in fase di dismissione lenta. Per nuovi progetti
considera Dialogflow CX.
