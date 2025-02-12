# Zadání úkolu pro Python Backend vývojáře - Todo aplikace

## Úvod

Vytvořte REST API pomocí Django REST framework pro todo aplikaci s následujícími endpointy, včetně možnosti nahrávat fotky ke každému úkolu.

## Technické specifikace

- Python 3.9+ a Django REST framework
- Dodržujte PEP 8, PEP 257 a PEP 484
- Používejte dvojité uvozovky místo jednoduchých
- Unit testy pro všechny endpointy
- Validační nástroje: Ruff (PEP 8, PEP 257), mypy (PEP 484)
- Pro ukládání dat použijte výchozí SQLite databázi, která je součástí Djanga
- Použijte knihovnu OpenCV pro zpracování obrázků (konverze a změna velikosti)

## Struktura úkolu

- `id`: int (auto-generované)
- `title`: string (povinné, max. 100 znaků)
- `description`: string (volitelné, max. 500 znaků)
- `due_date`: date (volitelné)
- `photo`: image (volitelné, umožňuje nahrání obrázku ke každému úkolu, obrázek je při uploadu automaticky konvertován na černobílý a zmenšen na maximální velikost 800x800 px)

## Endpointy

1. **GET `/api/tasks/`**

   - **Vstup**: Žádný
   - **Výstup**: JSON seznam všech úkolů
   - **Popis**: Vrátí kompletní seznam všech úkolů bez možnosti filtrování nebo stránkování.

2. **POST `/api/tasks/`**

   - **Vstup**: JSON s daty nového úkolu (`title`, `description`, `due_date`, `photo`)
   - **Výstup**: JSON vytvořeného úkolu včetně `id`
   - **Popis**: Vytvoří nový úkol. Důsledně kontrolujte přítomnost všech povinných parametrů (`title`). Pokud některý povinný parametr chybí, vraťte chybu 400 Bad Request s jasným popisem chybějícího parametru. Validujte vstupní data (např. maximální délku `title`). Pokud je nahrán obrázek, automaticky ho konvertujte pomocí OpenCV na černobílý a zmenšete na maximální velikost 800x800 px.

3. **GET `/api/tasks/{id}/`**

   - **Vstup**: ID úkolu v URL
   - **Výstup**: JSON s detaily úkolu, včetně URL obrázku (pokud je nahrán)
   - **Popis**: Vrátí detaily konkrétního úkolu. Pokud úkol neexistuje, vraťte 404.

4. **PUT `/api/tasks/{id}/`**

   - **Vstup**: ID úkolu v URL, JSON s daty úkolu (kompletními nebo částečnými)
   - **Výstup**: JSON aktualizovaného úkolu
   - **Popis**: Aktualizuje úkol. Pokud jsou poskytnuta všechna pole, provede se kompletní aktualizace. Pokud jsou poskytnuta jen některá pole, aktualizují se pouze tato pole. Validujte vstupní data. Pokud je aktualizován obrázek, znovu ho konvertujte pomocí OpenCV a zmenšete.

5. **DELETE `/api/tasks/{id}/`**

   - **Vstup**: ID úkolu v URL
   - **Výstup**: 204 No Content při úspěchu
   - **Popis**: Smaže úkol. Pokud úkol neexistuje, vraťte 404.

6. **GET `/api/tasks/nearest-deadline/`**

   - **Vstup**: Žádný
   - **Výstup**: JSON nejbližšího úkolu s nenulovým `due_date`
   - **Popis**: Vrátí úkol s nejbližším nenulovým termínem dokončení (`due_date`).

## LeetCode úlohy

Jako součást tohoto úkolu implementujte následující tři LeetCode úlohy jako další endpointy v aplikaci. Tyto úlohy testují různé aspekty algoritmického myšlení.

7. **POST `/api/leetcode/rotate-array/`**

   - **Vstup**: JSON obsahující pole čísel a počet rotací `k`
     ```json
     {
       "nums": [1, 2, 3, 4, 5, 6, 7],
       "k": 3
     }
     ```
   - **Výstup**: JSON s rotovaným polem
     ```json
     {
       "result": [5, 6, 7, 1, 2, 3, 4]
     }
     ```
   - **Popis**: Rotujte pole o `k` prvků doprava. Implementujte řešení s O(1) dodatečnou pamětí.

8. **POST `/api/leetcode/kth-largest/`**

   - **Vstup**: JSON obsahující pole čísel a `k`
     ```json
     {
       "nums": [3, 2, 1, 5, 6, 4],
       "k": 2
     }
     ```
   - **Výstup**: JSON s `k`-tým největším prvkem
     ```json
     {
       "result": 5
     }
     ```
   - **Popis**: Najděte `k`-tý největší prvek v neseřazeném poli. Snažte se dosáhnout lepší než O(n log n) časové složitosti.

9. **POST `/api/leetcode/longest-increasing-path/`**

   - **Vstup**: JSON obsahující 2D pole (matici) celých čísel
     ```json
     {
       "matrix": [
         [9, 9, 4],
         [6, 6, 8],
         [2, 1, 1]
       ]
     }
     ```
   - **Výstup**: JSON s délkou nejdelší rostoucí cesty
     ```json
     {
       "result": 4
     }
     ```
   - **Popis**: Najděte délku nejdelší rostoucí cesty v matici celých čísel. Implementujte efektivní řešení využívající dynamické programování a DFS.

Tyto LeetCode úlohy by měly být implementovány jako součást vaší Django aplikace. Ujistěte se, že jsou pokryty unit testy a dodržují stejné standardy kódu jako zbytek aplikace.

## Odevzdání

- GitHub repozitář s kódem
- Docker image
- README.md s instrukcemi pro spuštění
- Okomentované demo video (max. 10 minut), kde:
  - Projdete všechny implementované funkcionality
  - Ukážete, jak aplikace funguje
  - Okomentujete, jak jste postupovali při vývoji
  - Zmíníte, s čím jste měli problémy a jak jste je řešili
  - Případně uvedete, co byste udělali jinak, kdybyste měli více času

## Hodnotící kritéria

- Správnost implementace
- Kvalita kódu a dodržování PEP standardů
- Pokrytí testy
- Efektivita a rychlost
