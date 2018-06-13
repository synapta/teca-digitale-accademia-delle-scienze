# Comandi Utili

Per questo progetto python = python2

## Processo di upload

Per fare l'upload usare il comando

```
python reuploader.py /nome/della/directory
```

## Per generare csv libri di questa cartella (con indice)

```
python new_metadata_fetcher.py /nome/della/directory
```

## Per pathchare gli xml di archive

* <tt>XML_patcher.py</tt> patcha i file progressivamente (es. patcha solo i nuovi aggiunti dall'ultimo lancio); 
```
python3 XML_patcher.py
```
* <tt>XML_patcher_controller.py</tt> scarica gli xml di TUTTI i libri di ASTO e patcha quelli non validi.
```
python3 XML_patcher_controller.py
```
