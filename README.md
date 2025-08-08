# Reseptisovellus

Ruokareseptit
- Sovelluksessa käyttäjät pystyvät jakamaan ruokareseptejään. Reseptissä lukee tarvittavat ainekset ja valmistusohje.

- Käyttäjä pystyy luomaan tunnuksen ja kirjautumaan sisään sovellukseen.

- Käyttäjä pystyy lisäämään reseptejä ja muokkaamaan ja poistamaan niitä.

- Käyttäjä näkee sovellukseen lisätyt reseptit.

- Käyttäjä pystyy etsimään reseptejä hakusanalla.

- Käyttäjäsivu näyttää, montako reseptiä käyttäjä on lisännyt ja listan käyttäjän lisäämistä resepteistä.

- Käyttäjä pystyy valitsemaan reseptille yhden tai useamman luokittelun (esim. alkuruoka, intialainen, vegaaninen).

- Käyttäjä pystyy antamaan reseptille kommentin ja arvosanan. Reseptistä näytetään kommentit ja keskimääräinen arvosana.

## Sovelluksen asentamisohjeet
Varmista, että sinulla on ladattuna python3 etukäteen.

1. Kloonaa repositorio
```bash
git clone https://github.com/hodelma/Reseptisovellus.git
```


2. Ota käyttöön virtuaaliympäristö komennolla
```bash
python3 -m venv venv
```


3. Siirry virtuaaliympäristöön
```bash
source venv/bin/activate
```

4. Asenna ```flask```-kirjasto
```bash
pip install flask
```


5. Luo tietokanta komennolla
```bash
sqlite3 database.db < schema.sql
sqlite3 database.db < init.sql
```


6. Suorita flask sovellus komennolla
```bash
flask run
```

7. Sovelluksen suoritus debug tilassa (vapaavalintainen)
```bash
flask run --debug
```
