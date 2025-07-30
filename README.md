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

# Sovelluksen asentamisohjeet
Varmista, että sinulla on ladattuna python3

Kloonaa repositorio<br>
```git clone git@github.com:hodelma/Reseptisovellus.git```


Ota käyttöön virtuaaliympäristö komennolla<br>
```python3 -m venv venv```<br>
ja suorita sitten<br>
```source venv/bin/activate```


Luo tietokanta komennolla<br>
```database.db < schema.sql```


Suorita flask sovellus komennolla<br>
```flask run```<br>
tai vaihtoehtoisesti debug tilassa<br>
```flask run --debug```
