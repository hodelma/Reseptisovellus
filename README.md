# Reseptisovellus

## Tervetuloa käyttämään ruokareseptisovellusta! 🍽
<br>

**Tässä sovelluksessa tulee olemaan seuraavanlaiset ominaisuudet:**
<br>
- Sovelluksessa käyttäjät pystyvät jakamaan ruokareseptejään. Reseptissä lukee tarvittavat ainekset ja valmistusohje.

- Käyttäjä pystyy luomaan tunnuksen ja kirjautumaan sisään sovellukseen.

- Käyttäjä pystyy lisäämään, muokkaamaan ja poistamaan reseptejä.

- Käyttäjä näkee sovellukseen lisätyt reseptit.

- Käyttäjä pystyy etsimään reseptejä hakusanalla.

- Käyttäjäsivu näyttää, montako reseptiä käyttäjä on lisännyt ja listan käyttäjän lisäämistä resepteistä.

- Käyttäjä pystyy valitsemaan reseptille yhden tai useamman luokittelun (esim. alkuruoka, pääruoka, gluteeniton, vegaaninen).

- Käyttäjä pystyy antamaan reseptille kommentin ja arvosanan. Reseptistä näytetään kommentit ja keskimääräinen arvosana.
<br><br>
## Sovelluksen asentamisohjeet
*Varmista, että sinulla on ladattuna python3 etukäteen. Sovellus on kehitetty Python 3.12.3 versiolla.*
<br><br>

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


5. Luo tietokanta komennoilla
```bash
sqlite3 database.db < schema.sql
sqlite3 database.db < init.sql
```


6. Suorita flask-sovellus komennolla
```bash
flask run
```

7. Sovelluksen suoritus debug-tilassa (vapaavalintainen)
```bash
flask run --debug
```
<br>

## Testidataraportti

<br>

Sovellusta on testattu suurella tietomäärällä `seed.py` tiedoston avulla ja se toimii tehokkaasti.

Testidatan suuruus:

`USER_COUNT = 1000`

`RECIPE_COUNT = 10**5`

`COMMENT_COUNT = 10**6`

<br>

Ajat eri tärkeissä operaatioissa ennen indeksin lisäämistä:

- Etusivun lataaminen (0.04s - 0.05s)
- Kirjautuminen / rekisteröinti (0.10s-0.15s)
- Reseptien selaaminen sivutuksen avulla (0.0s - 0.02s)
- Reseptin avaaminen (0.00s - 0.03s)
- Reseptin kommenttikentän avaaminen (0.00s - 0.03s)
- Käyttäjäprofiilin avaaminen ja sivujen selaus (0.01s - 0.03s)
- Reseptin / kommentin lisääminen (0.01s - 0.02s)
- Reseptin /kommentin poistaminen (0.00s - 0.02s)
- Reseptin / kommentin muokkaaminen (0.0s - 0.02s)
- Reseptin hakeminen (0.00s - 0.02s)

<br>

Indeksien lisääminen jälkeen jokaisen operaation ajankäyttö oli välillä (0.0s - 0.01s) <br> <br>
`CREATE INDEX idx_recipes_type_id ON recipes(type_id);`<br>
`CREATE INDEX idx_recipes_diet_id ON recipes(diet_id);`<br>
`CREATE INDEX idx_recipes_title ON recipes(title);`<br>
`CREATE INDEX idx_comments_recipe_id ON comments(recipe_id);`<br>
`CREATE INDEX idx_comments_user_id ON comments(user_id);`<br>
`CREATE INDEX idx_recipes_user_id ON recipes(user_id);`
