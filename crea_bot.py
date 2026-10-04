"""
Generatore del progetto GitHub per CostyCNC Chatbot
Crea tutti i file necessari in una cartella pronta per il push su GitHub
"""
import os
import json
import zipfile
import shutil
import uuid

# ==========================================
# CONFIGURAZIONE
# ==========================================
PROJECT_DIR = "costycnc-chatbot"

# ==========================================
# INTENT DEL BOT
# ==========================================
intents = [
    {
        "name": "saluto",
        "phrases": ["ciao", "buongiorno", "buonasera", "salve", "hey", "ehi"],
        "responses": ["Ciao! Sono l'assistente virtuale di CostyCNC.\nPosso aiutarti con:\n- Conversione SVG in G-code\n- Informazioni sulle macchine CNC\n- Prezzi e spedizioni\n- Installazione software\n\nCome posso aiutarti?"]
    },
    {
        "name": "saluto_finale",
        "phrases": ["arrivederci", "a presto", "bye"],
        "responses": ["Ciao! Torna quando vuoi.\nBuon lavoro con CostyCNC!"]
    },
    {
        "name": "ringraziamento",
        "phrases": ["grazie", "grazie mille", "ti ringrazio", "perfetto grazie"],
        "responses": ["Prego! Se hai altre domande sono qui."]
    },
    {
        "name": "conferma_si",
        "phrases": ["si", "sì", "ok", "va bene", "certo", "esatto", "giusto"],
        "responses": ["Perfetto! Dimmi pure cosa ti serve."]
    },
    {
        "name": "conferma_no",
        "phrases": ["no", "non voglio", "non mi interessa", "no grazie"],
        "responses": ["Va bene! Se cambi idea sono qui."]
    },
    {
        "name": "svg_to_gcode",
        "phrases": [
            "io ho i file svg come li porto in g code?",
            "da svg a gcode",
            "come converto svg in gcode",
            "convertire svg in gcode",
            "svg to gcode",
            "trasformare svg in gcode",
            "ho un file svg e voglio fare gcode",
            "come faccio a passare da svg a gcode"
        ],
        "responses": ["Per convertire SVG in G-code usa il tool CostyCNC:\n\n1. Vai su https://www.costycnc.it/cm8\n2. Clicca su 'Paste SVG da Inkscape'\n3. Incolla il tuo SVG (Ctrl+V)\n4. Regola dimensione e DPI\n5. Premi 'Create GCODE'\n6. Salva con 'Save gcode'\n\nIl tool e gratuito e funziona nel browser!"]
    },
    {
        "name": "image_to_gcode",
        "phrases": [
            "come converto un'immagine in gcode",
            "da immagine a gcode",
            "image to gcode",
            "ho una foto come la trasformo in gcode",
            "convertire jpg in gcode",
            "convertire png in gcode"
        ],
        "responses": ["Per convertire un'immagine in G-code:\n\n1. Vai su https://www.costycnc.it/cm8\n2. Carica l'immagine (JPG, PNG, BMP, SVG)\n3. Regola DPI e dimensioni\n4. Clicca 'Create GCODE'\n\nIl tool estrae i percorsi e li ottimizza automaticamente."]
    },
    {
        "name": "Info_Prezzi",
        "phrases": [
            "quanto costa", "qual e il prezzo", "prezzi", "quanto viene",
            "mi dici il costo", "prezzo della macchina", "quanto costa la cnc", "listino prezzi"
        ],
        "responses": ["Ecco i prezzi delle nostre macchine CostyCNC:\n\nHOBBY  - 150x30x8 cm  - da 125 EUR\nMINI   - 150x40x15 cm - da 210 EUR\nMEDIA  - 250x50x30 cm - da 410 EUR\nXBIG   - 250x90x90 cm - da 600 EUR\n\nI prezzi variano in base alla destinazione.\nPer dettagli: https://www.costycnc.it"]
    },
    {
        "name": "info_software_installazione",
        "phrases": [
            "come installo il software", "installazione", "come si installa",
            "devo installare qualcosa", "programma da scaricare"
        ],
        "responses": ["Il programma CostyCNC e offline e gratuito:\n\n1. Vai su https://www.costycnc.it/cm8\n2. Scarica 'costycnc-img-to-gcode.zip'\n3. Decomprimi il file\n4. Apri 'index.html' nel browser\n\nNon serve installazione!"]
    },
    {
        "name": "info_firmware",
        "phrases": ["firmware", "che firmware usa", "devo aggiornare il firmware", "grbl", "mks dlc32"],
        "responses": ["Le nostre macchine usano:\n- Scheda: MKS DLC32\n- Firmware: GRBL compatibile\n- Connessione: WiFi, USB, SD\n\nPer il firmware aggiornato:\nhttps://www.costycnc.it/firmware"]
    },
    {
        "name": "info_specifiche",
        "phrases": ["che specifiche ha", "caratteristiche tecniche", "dimensioni area di lavoro", "che motori usa", "scheda di controllo"],
        "responses": ["Specifiche tecniche CostyCNC:\n\n- Motori: 28BYJ-48 / NEMA 17\n- Driver: A4988\n- Scheda: MKS DLC32 (WiFi + USB + SD)\n- Filo caldo: Nichrome 0,2mm\n- Alimentazione: 12V o 24V"]
    },
    {
        "name": "info_taglio_polistirolo",
        "phrases": ["che materiali taglia", "posso tagliare polistirolo", "taglia polistirene", "che spessore puo tagliare", "taglio a filo caldo"],
        "responses": ["Le nostre macchine tagliano:\n- Polistirolo (EPS)\n- Polistirene espanso (XPS)\n- Materiali espansi leggeri\n\nIl taglio e a filo caldo (hot wire)."]
    },
    {
        "name": "info_rotary_table",
        "phrases": ["tavola rotante", "piano rotante", "rotary table", "posso tagliare forme tonde"],
        "responses": ["Si! CostyCNC supporta la tavola rotante per:\n- Taglio di forme cilindriche\n- Coni e sfere\n- Forme 3D con rotazione\n\nSi attiva dal pannello 'Rotate Table' nel software."]
    },
    {
        "name": "info_spedizioni",
        "phrases": ["spedite", "come spedite", "quanto tempo per la consegna", "spedizione", "consegna", "quanto ci mette ad arrivare"],
        "responses": ["Spediamo in tutta Italia, Europa e nel mondo.\n\n- Italia: 2-4 giorni lavorativi\n- Europa: 4-7 giorni lavorativi\n- Mondo: 7-15 giorni lavorativi\n\nDisponibile pagamento in contrassegno."]
    },
    {
        "name": "info_garanzia",
        "phrases": ["garanzia", "c'e garanzia", "cosa succede se si rompe", "assistenza", "reso", "rimborso"],
        "responses": ["Tutte le nostre macchine hanno garanzia.\nPer resi e rimborsi consulta:\nhttps://www.costycnc.it/politica-di-reso/\n\nPer assistenza tecnica scrivici direttamente."]
    },
    {
        "name": "info_contatti",
        "phrases": ["come vi contatto", "numero di telefono", "email", "contatti", "dove siete"],
        "responses": ["Puoi contattarci tramite:\n- Sito: https://www.costycnc.it\n- Facebook: facebook.com/costelcnc\n- YouTube: youtube.com/@bobyca2003\n- eBay: ebay.it/str/costycnc"]
    },
    {
        "name": "info_tutorial",
        "phrases": ["ci sono tutorial", "come si usa", "video tutorial", "guida", "manuale"],
        "responses": ["Si! Trovi tutorial su:\n- YouTube: https://www.youtube.com/@bobyca2003\n- Blog: https://costycnc1.blogspot.com/\n- Tutorial sito: https://www.costycnc.it/tutorial"]
    },
    {
        "name": "info_acquisto",
        "phrases": ["come compro", "come acquisto", "dove comprare", "posso pagare con paypal"],
        "responses": ["Puoi acquistare su:\n- eBay: https://www.ebay.it/str/costycnc\n- PayPal dal nostro sito\n- Contrassegno (solo Italia)"]
    }
]


# ==========================================
# CREA IL PROGETTO GITHUB
# ==========================================
def create_github_project():
    if os.path.exists(PROJECT_DIR):
        shutil.rmtree(PROJECT_DIR)
    
    os.makedirs(PROJECT_DIR)
    
    # --- README.md ---
    readme = """# CostyCNC Chatbot - Dialogflow ES

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
"""
    with open(os.path.join(PROJECT_DIR, "README.md"), "w", encoding="utf-8") as f:
        f.write(readme)
    
    # --- TUTORIAL.md ---
    tutorial = """# Tutorial: Crea un chatbot con Dialogflow ES

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
"""
    with open(os.path.join(PROJECT_DIR, "TUTORIAL.md"), "w", encoding="utf-8") as f:
        f.write(tutorial)
    
    # --- TROUBLESHOOTING.md ---
    troubleshooting = """# Dialogflow ES - Troubleshooting

Tutti i problemi che abbiamo incontrato durante la creazione di un chatbot
Dialogflow ES, con le soluzioni testate.

## Indice

1. `'X' is not a valid intent ID. Must be a UUID`
2. `can not be passed into JsonElement`
3. `BadRequestException` durante l'import
4. `Nothing to import` - ZIP non letto
5. `Permission 'dialogflow.agents.get' not granted`
6. Vecchio URL `console.dialogflow.com/api-client/demo/embedded` non funziona
7. Il bot risponde sempre con il Fallback
8. Il progetto Google Cloud non appare nella lista
9. Cartella doppia nello ZIP
10. Pulsante IMPORT grigio/disabilitato

---

## 1. `'X' is not a valid intent ID. Must be a UUID`

### Errore
    Validate intent with display name 'saluto_finale' failed because of the following reasons:
    'intent-017' is not a valid intent ID. Must be a UUID.

### Causa
Stai usando ID tipo `intent-001` invece di veri **UUID v4**.

### Soluzione
Sostituisci:

    "id": f"intent-{counter:03d}",   # SBAGLIATO

con:

    import uuid
    "id": str(uuid.uuid4()),         # CORRETTO

---

## 2. `can not be passed into JsonElement`

### Errore
    This file 'intents/image_to_gcode_user_says.json' can not be passed into JsonElement.
    Check if this is in valid json format.

### Causa
Il **nome del file delle training phrases** e sbagliato. Dialogflow ES e
estremamente pignolo sul nome file.

### Nomi SBAGLIATI
- `image_to_gcode_user_says.json` (singolare, senza "it")
- `image_to_gcode_usersays.json` (manca "_it")
- `image_to_gcode_user_says_it.json` ("user_says" invece di "usersays")

### Nome CORRETTO

    {nome_intent}_usersays_it.json

Esempi corretti:

    image_to_gcode_usersays_it.json      OK
    svg_to_gcode_usersays_it.json        OK
    conferma_no_usersays_it.json         OK

Deve essere tutto attaccato: **usersays** + **_it**.

---

## 3. `BadRequestException` durante l'import

### Cause possibili
- **BOM UTF-8** all'inizio del file
- **Apostrofi** `'` non gestiti
- **Emoji** nei testi
- JSON con virgole doppie o parentesi sbilanciate
- File troppo grande (> 10 MB)

### Soluzione
1. Apri con **Notepad++**
2. Menu **Encoding** -> **UTF-8** (NON "UTF-8 BOM")
3. Salva
4. Valida JSON su [jsonlint.com](https://jsonlint.com)

---

## 4. `Nothing to import` - ZIP non letto

### Cause
- Cartella doppia nello ZIP (es. `costycnc-bot/costycnc-bot/`)
- Manca `agent.json` nella root
- Manca cartella `intents/`

### Struttura corretta

    costycnc-bot.zip
    +-- costycnc-bot/         <- UNA SOLA cartella
        +-- agent.json
        +-- package.json
        +-- intents/
            +-- saluto.json
            +-- saluto_usersays_it.json

### Struttura SBAGLIATA

    costycnc-bot.zip
    +-- costycnc-bot/
        +-- costycnc-bot/     <- DOPPIA!
            +-- agent.json
            +-- intents/

---

## 5. `Permission 'dialogflow.agents.get' not granted`

### Errore
    com.google.apps.framework.auth.IamPermissionDeniedException:
    Permission 'dialogflow.agents.get' not granted to cloud-ml-dialogflow-frontend@prod.google.com,
    because no ALLOW or ALLOW_WITH_LOG rule includes that permission.

### Causa
Non hai i permessi IAM sul progetto Google Cloud.
**Oppure stai lavorando nel progetto Google Cloud SBAGLIATO!**

### Soluzione passo-passo

**Passo 1** - Trova il Project ID corretto:
Dialogflow -> Settings -> **General** -> copia il **Project ID**

**Passo 2** - Vai su [Google Cloud Console](https://console.cloud.google.com)

**Passo 3** - In alto a sinistra, seleziona il progetto **corretto**
Se non appare -> vedi problema 8

**Passo 4** - Menu -> **IAM e amministrazione** -> **IAM**

**Passo 5** - Trova il tuo indirizzo email -> clicca matita

**Passo 6** - Aggiungi ruoli:
- **Dialogflow API Admin**
- **Dialogflow Console Agent Editor**
- **Editor** (generico)

**Passo 7** - **SAVE** -> torna in Dialogflow -> ricarica -> riprova

---

## 6. Vecchio URL `console.dialogflow.com/api-client/demo/embedded` non funziona

### Errore
    La pagina web all'indirizzo https://console.dialogflow.com/api-client/demo/embedded/...
    potrebbe essere temporaneamente non disponibile oppure e stata permanentemente
    spostata a un nuovo indirizzo web.

### Causa
Google ha **dismesso** il vecchio servizio "web demo".

### Soluzione - Usa Dialogflow Messenger

1. Dialogflow -> **Integrations** -> **Dialogflow Messenger**
2. Clicca **ENABLE**
3. Copia il codice:

    <script src="https://www.gstatic.com/dialogflow-console/fast/messenger/bootstrap.js?v=1"></script>
    <df-messenger
      intent="WELCOME"
      chat-title="CostyCNC"
      agent-id="IL_TUO_AGENT_ID"
      language-code="it">
    </df-messenger>

**NON confondere `agent-id` con il Project ID!**
- `agent-id` = UUID tipo `9378968c-5941-48e8-95e1-8014f7fa02f5`
- `Project ID` = stringa tipo `costycnc-bot-lxxc`

---

## 7. Il bot risponde sempre con il Fallback

### Cause
- Training phrases **non importate**
- **Soglia ML troppo alta** (default 0.7)
- Il modello deve **reindicizzare** (1-2 minuti)

### Soluzione
1. **Verifica training phrases:** apri l'intent -> controlla le frasi
2. **Clicca SAVE** nell'intent -> forza riaddestramento
3. **Aspetta 2 minuti**
4. **Riprova**
5. Se ancora non funziona -> **abbassa soglia ML:**
   Settings -> **ML Settings** -> **Classification threshold** -> `0.4`

---

## 8. Il progetto Google Cloud non appare nella lista

### Sintomo
Nella schermata "Seleziona un progetto" non vedo il progetto `costycnc-bot`.

### Cause
1. Loggato con **account Google diverso**
2. Progetto in **organizzazione aziendale** non accessibile
3. Agent Dialogflow **trial/temporaneo** senza progetto Cloud
4. Nome progetto **completamente diverso** (es. "My First Project")

### Soluzione

**Verifica 1** - Controlla che l'account sia lo stesso in Dialogflow e Cloud Console

**Verifica 2** - Trova il Project ID reale:
Dialogflow -> Settings -> **General** -> copia il **Project ID**

**Verifica 3** - Cerca per ID:
Nella schermata "Seleziona progetto", scrivi il **Project ID esatto** nel campo di ricerca

### Se ancora non appare -> Crea un nuovo progetto
1. [Google Cloud Console](https://console.cloud.google.com)
2. **Seleziona un progetto** -> **NUOVO PROGETTO**
3. Nome: `costycnc-chatbot`
4. Crea
5. Torna in Dialogflow -> crea un nuovo agent selezionando questo progetto
6. Reimporta lo ZIP

---

## 9. Cartella doppia nello ZIP

### Causa
Hai eseguito lo script Python **dentro** una cartella che si chiama gia come l'agent.

### Soluzione

    # SBAGLIATO: esegui dentro costycnc-bot/
    cd costycnc-bot/
    python crea_bot.py
    # -> crea costycnc-bot/costycnc-bot/

    # CORRETTO: esegui da cartella neutra
    cd /Desktop/lavoro/
    python crea_bot.py
    # -> crea lavoro/costycnc-bot/

---

## 10. Pulsante IMPORT grigio/disabilitato

### Causa
Hai caricato lo ZIP ma non hai digitato la conferma.

### Soluzione
Nel campo di testo scrivi: `IMPORT` (tutto maiuscolo) -> il pulsante diventa cliccabile.

---

## Checklist finale prima dell'import

| # | Verifica | OK? |
|---|----------|-----|
| 1 | Tutti gli ID sono UUID v4 | [ ] |
| 2 | File training si chiamano `{name}_usersays_it.json` | [ ] |
| 3 | Nessun file `_user_says.json` | [ ] |
| 4 | ZIP ha una sola cartella radice | [ ] |
| 5 | `agent.json` presente | [ ] |
| 6 | File salvati come UTF-8 senza BOM | [ ] |
| 7 | JSON validati con jsonlint.com | [ ] |
| 8 | Campo `type` e `"0"` (stringa) | [ ] |
| 9 | Campi `title`, `textToSpeech`, `condition` presenti | [ ] |
| 10 | Numero file in `intents/` = 2 x numero intent | [ ] |
"""
    with open(os.path.join(PROJECT_DIR, "TROUBLESHOOTING.md"), "w", encoding="utf-8") as f:
        f.write(troubleshooting)
    
    # --- LICENSE ---
    license_text = """MIT License

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
        f.write(license_text)
    
    # --- .gitignore ---
    gitignore = """# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/

# ZIP generati (non vanno su GitHub)
costycnc-bot/
costycnc-bot.zip

# OS
.DS_Store
Thumbs.db

# IDE
.vscode/
.idea/
*.swp
"""
    with open(os.path.join(PROJECT_DIR, ".gitignore"), "w", encoding="utf-8") as f:
        f.write(gitignore)
    
    # --- Copia crea_bot.py nel progetto ---
    script_path = os.path.abspath(__file__)
    if os.path.exists(script_path):
        shutil.copy(script_path, os.path.join(PROJECT_DIR, "crea_bot.py"))
    
    print("[OK] Progetto GitHub creato: " + PROJECT_DIR + "/")
    print()
    print("Struttura:")
    print("   " + PROJECT_DIR + "/")
    print("   |-- README.md              (panoramica progetto)")
    print("   |-- TUTORIAL.md            (tutorial passo-passo)")
    print("   |-- TROUBLESHOOTING.md     (10 problemi + soluzioni)")
    print("   |-- LICENSE                (MIT)")
    print("   |-- .gitignore")
    print("   +-- crea_bot.py            (script generatore ZIP)")


# ==========================================
# CREA IL BOT DIALOGFLOW (ZIP IMPORTABILE)
# ==========================================
AGENT_NAME = "costycnc-bot"
ZIP_NAME = "costycnc-bot.zip"

def create_dialogflow_zip():
    if os.path.exists(AGENT_NAME):
        shutil.rmtree(AGENT_NAME)
    
    os.makedirs(os.path.join(AGENT_NAME, "intents"))
    
    agent = {
        "id": str(uuid.uuid4()),
        "description": "Assistente virtuale CostyCNC",
        "language": "it",
        "shortDescription": "Bot assistenza CNC polistirolo",
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
                    "lang": "it",
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
        
        usersays = [{
            "id": str(uuid.uuid4()),
            "data": [{"text": phrase, "userDefined": False}],
            "isTemplate": False,
            "count": 0,
            "lang": "it",
            "updated": 0
        } for phrase in intent["phrases"]]
        
        usersays_filename = intent["name"] + "_usersays_it.json"
        with open(os.path.join(AGENT_NAME, "intents", usersays_filename), "w", encoding="utf-8") as f:
            json.dump(usersays, f, ensure_ascii=False, indent=2)
    
    if os.path.exists(ZIP_NAME):
        os.remove(ZIP_NAME)
    with zipfile.ZipFile(ZIP_NAME, "w", zipfile.ZIP_DEFLATED) as z:
        for root, dirs, files in os.walk(AGENT_NAME):
            for file in files:
                fp = os.path.join(root, file)
                z.write(fp, os.path.relpath(fp, "."))
    
    print("[OK] ZIP Dialogflow creato: " + ZIP_NAME)
    print("Contiene " + str(len(intents)) + " intent (" + str(len(intents)*2) + " file totali)")


# ==========================================
# MAIN
# ==========================================
if __name__ == "__main__":
    print("=" * 60)
    print("GENERATORE PROGETTO COSTYCNC CHATBOT")
    print("=" * 60)
    print()
    
    print("[1/2] Creo la cartella del progetto GitHub...")
    create_github_project()
    print()
    
    print("[2/2] Genero lo ZIP importabile in Dialogflow...")
    create_dialogflow_zip()
    print()
    
    print("=" * 60)
    print("COMPLETATO!")
    print("=" * 60)
    print()
    print("Trovi tutto nella cartella: " + PROJECT_DIR)
    print("ZIP per Dialogflow: " + ZIP_NAME)
