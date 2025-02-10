# 📸 Instagram Spotted Bot

Instagram Spotted Bot è uno strumento automatizzato progettato per gestire le pagine "Spotted" su Instagram. Il bot raccoglie i messaggi diretti ricevuti, li filtra e pubblica automaticamente quelli appropriati come immagini sul tuo profilo.

Una pagina "_Spotted_" su Instagram è un profilo dedicato alla condivisione di messaggi inviati in forma anonima dagli utenti, spesso riguardanti osservazioni, confessioni o segnalazioni relative a una specifica comunità o luogo, come università, scuole o città. Gli amministratori della pagina ricevono questi messaggi tramite direct message e, dopo averli moderati, li pubblicano mantenendo l'anonimato dell'autore. Questo fenomeno è particolarmente diffuso in ambito universitario, dove gli studenti utilizzano le pagine "Spotted" per condividere esperienze, cercare persone incontrate casualmente o esprimere opinioni in modo anonimo.

## 🌟 Caratteristiche

- **Raccolta Automatica dei Messaggi:** Recupera i messaggi non letti dal tuo account Instagram.

- **Filtraggio Intelligente:** Applica criteri di filtro per selezionare i messaggi idonei alla pubblicazione.

- **Generazione di Immagini:** Converte i messaggi selezionati in immagini pronte per la condivisione.

- **Pubblicazione Programmata:** Pubblica automaticamente le immagini generate sul tuo profilo Instagram.

## 📋 Prerequisiti

- **Python 3.8+:** Assicurati di avere installato Python nella versione 3.8 o successiva. Puoi scaricarlo qui.

- **Pip:** Gestore di pacchetti per Python. Solitamente incluso con Python, ma puoi verificarne la presenza eseguendo:
```
pip --version
```
## 🛠️ Installazione

1. Clona il Repository:
```bash
git clone https://github.com/itsPinguiz/instagram-spotted-bot.git
cd instagram-spotted-bot
```

2. Crea un Ambiente Virtuale:
```bash
python3 -m venv venv
source venv/bin/activate  # Su Windows: venv\Scripts\activate
```

3. Installa le Dipendenze:
```bash
pip install -r requirements.txt
```

## 🔧 Configurazione

1. Credenziali Instagram:

- Rinomina `ig_settings.example.json` in `ig_settings.json`.

- Apri `ig_settings.json` e inserisci il tuo `username` e `password` di Instagram.

2. Parametri del Bot:

- Personalizza le impostazioni nel file `ig_settings.json` secondo le tue esigenze, come i filtri per i messaggi e le opzioni di pubblicazione.

## 🚀 Utilizzo

Avvia il bot eseguendo lo script principale:
```
python app.py
```
Il bot inizierà a raccogliere, filtrare e pubblicare automaticamente i messaggi ricevuti nei Direct di Instagram.

## 📂 Struttura del Progetto

- `app.py`: Script principale per l'esecuzione del bot.

- `botConsole.py`: Modulo per l'interfaccia della console del bot.

- `botPoster.py`: Gestisce la pubblicazione dei post su Instagram.

- `botTimer.py`: Modulo per la gestione della temporizzazione delle operazioni.

- `utilities/`: Contiene funzioni e classi di supporto.

- `images/`: Directory per le immagini generate dai messaggi.

- `ig_settings.json`: File di configurazione per le credenziali e le impostazioni del bot.

--- 

_Nota_: L'utilizzo di bot su Instagram potrebbe violare i termini di servizio della piattaforma. Usa questo software a tuo rischio e pericolo.
