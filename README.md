# Y2_2022_78549
Joni's sick annotation program

## Esittely
Ohjelma, jonka avulla voi annotoida kuvia ja selata jo valmiiksi annotoituja kuvia. Annotoidut kuvat pystyt tuomaan omaan projektiisi importtaamalla dataset.py tiedostosta ImageAnnotationsDataset funktion.

## Tiedosto- ja kansiorakenne

- images
  - annotated (Kansio annotoiduille kuville)
  - not_annotated (Kansio, johon tallennat kuvat, jotka haluat annotoida)
- src
  - ui
    - tests (sisältää testi tiedostot)
    - utils (sisältää tiedostot apufunktioille)
    + gui tiedostot
  - dataset.py
- doc

## Asennusohje

Asenna seuraavat kirjastot komennolla pip install ___
- torch
- sqlite3
- torchvision
- pandas

Lisäksi tarvitset PyQT5 krjaston

## Käyttöohje

Ohjelma käynnistetään komentoriviltä komennolla 
```
python main.py
```
Ohjelman käynnistyttyä se luo koneellesi vaadittavat kansiot, joihin annotoitavia kuvia voit siirtää. Kansioon images/not_annotated, sinun tulee siirtää kuvat, jotka haluat annotoida.

Siirrettyäsi kuvat kansioon, voit alkaa annnotoida kuvia painamalla päävalikon näppäintä "Annotate". Ensin käyttäjän tulee kirjoittaa vasemman yläkulman tekstilaatikkoon annotoitavan objektin nimi, jonka jälkeen käyttäjä voi maalata kuvasta kohdan jonka haluaa annotoida. Seuraavaan kuvaan pääsee klikkaamalla painiketta "Change Image".

Annotoituja kuvia käyttäjä voi selata painamalla päävalikon näppäintä Explore Annotations".

Annotoidut kuvat käyttäjä voi viedä projektiinsa:
```python
from dataset.py import ImageAnnotationsDataset
```
