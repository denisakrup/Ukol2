import requests
import json

# Zeptej se uživatele na IČO
ico = input("Zadej IČO subjektu: ")

# Sestav URL pro GET požadavek
url = f"https://ares.gov.cz/ekonomicke-subjekty-v-be/rest/ekonomicke-subjekty/{ico}"

# Odešli GET požadavek a zpracuj odpověď
response = requests.get(url)
data = response.json()

# Získání informací o obchodním jméně a adrese sídla
obchodni_jmeno = data.get("obchodniJmeno")
adresa_sidla = data.get("textovaAdresa")

# Vypiš získané informace
print(obchodni_jmeno)
print(adresa_sidla)

#------------cast2------------#

# Zeptej se uživatele na název subjektu
nazev_subjektu = input("Zadejte název subjektu: ")

# Sestav JSON data pro POST požadavek
data = '{"obchodniJmeno": "' + nazev_subjektu + '"}'

# Pokud název obsahuje diakritiku, zakóduj data jako UTF-8
if any(ord(char) > 127 for char in nazev_subjektu):
    data = data.encode("utf-8")

# Nastav hlavičky pro požadavek
headers = {
    "accept": "application/json",
    "Content-Type": "application/json",
}

# Odešli POST požadavek na vyhledání podle názvu
response = requests.post("https://ares.gov.cz/ekonomicke-subjekty-v-be/rest/ekonomicke-subjekty/vyhledat", headers=headers, data=data)

# Zpracuj JSON odpověď
data = response.json()
pocet_nalezenych = data.get("pocetCelkem")
subjekty = data.get("ekonomickeSubjekty")

# Přidej POST požadavek na stažení číselníku právních forem
data = '{"kodCiselniku": "PravniForma", "zdrojCiselniku": "res"}'
response = requests.post("https://ares.gov.cz/ekonomicke-subjekty-v-be/rest/ciselniky-nazevniky/vyhledat", headers=headers, data=data)

# Zpracuj JSON odpověď
ciselnik_data = response.json()
ciselnik = ciselnik_data.get("ciselniky")[0]  # První (a jediný) číselník
polozky_ciselniku = ciselnik.get("polozkyCiselniku")

# Funkce pro nalezení právní formy podle kódu
def find_legal_form(kod, polozky_ciselniku):
    for polozka in polozky_ciselniku:
        if polozka.get("kod") == kod:
            return polozka.get("nazev")
    return "Neznámá právní forma"

# Vypiš obchodní jména všech nalezených subjektů, jejich IČO a právní formu
print(f"Nalezeno subjektů: {pocet_nalezenych}")
for subjekt in subjekty:
    obchodni_jmeno = subjekt.get("obchodniJmeno")
    ico = subjekt.get("ico")
    pravni_forma_kod = subjekt.get("pravniForma")
    pravni_forma_nazev = find_legal_form(pravni_forma_kod, polozky_ciselniku)
    print(f"{obchodni_jmeno}, IČO: {ico}, Právní forma: {pravni_forma_nazev}")