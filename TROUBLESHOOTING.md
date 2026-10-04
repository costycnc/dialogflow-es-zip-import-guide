# Dialogflow ES - Troubleshooting

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
