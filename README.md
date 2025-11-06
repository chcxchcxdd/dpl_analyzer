# Analizator DPL - Zagęszczenie gruntu v2.0

Prosta, ale potężna aplikacja desktopowa (Windows/Linux/macOS) do analizy danych z sondowań DPL (lekką sondą dynamiczną). Umożliwia szybkie wprowadzanie danych pomiarowych (`N₁₀`), automatyczne obliczanie wskaźnika zagęszczenia (`Id`) i stanu gruntu (`Is`) oraz generowanie profesjonalnych, gotowych do publikacji wykresów.

![Przykładowy interfejs aplikacji](https://i.imgur.com/TwojeIDObrazka.png) 
*(Sugestia: Zastąp ten link zrzutem ekranu Twojej aplikacji)*

## 🚀 Główne funkcjonalności

* **Wprowadzanie danych:**
    * Ręczne dodawanie punktów pomiarowych (Głębokość i `N₁₀`).
    * Automatyczne generowanie punktów co 10 cm w zadanym zakresie (np. od 0.2 m do 5.0 m).
* **Obliczenia geotechniczne:**
    * Automatyczne obliczanie wskaźnika zagęszczenia (`Id`) oraz stanu gruntu (`Is`) na podstawie wprowadzonych wartości `N₁₀`.
    * Obliczenia bazują na wzorach:
        * $I_d = 0.429 \cdot \log_{10}(N_{10}) + 0.071$
        * $I_s = I_d \cdot 0.188 + 0.845$
* **Wizualizacja danych:**
    * Generowanie czytelnego wykresu słupkowego liczby udarów `N₁₀` w funkcji głębokości.
    * Możliwość dodania **profilu geologicznego** (opisy warstw) obok głównego wykresu.
    * Możliwość dodania **tabeli z wynikami** (`Id` oraz `Is`) bezpośrednio na wykresie.
* **Zarządzanie danymi:**
    * **Edycja w locie:** Szybka edycja wartości `N₁₀` bezpośrednio w tabeli (podwójne kliknięcie, `F2` lub `Enter`).
    * Pełna obsługa nawigacji klawiaturą podczas edycji (przechodzenie do następnego/poprzedniego punktu).
    * Sortowanie danych w tabeli po dowolnej kolumnie (lp., Głębokość, `N₁₀`, `Id`, `Is`).
    * Usuwanie pojedynczych punktów lub czyszczenie całych tabel.
* **Interfejs i Eksport:**
    * Nowoczesny, responsywny, ciemny interfejs użytkownika (oparty o `ttk.Style`).
    * **Eksport wykresu** do wysokiej jakości plików **PNG**, **JPG** lub **PDF** (w formacie A4 poziomo, 300 DPI).

---

## 🛠️ Wymagania

* **Python 3.x** (zalecany 3.6+): Podstawowy interpreter języka.
* **Matplotlib**: Niezbędna biblioteka używana do generowania i wyświetlania wykresów.

### ⚙️ Instalacja zależności

Aby zainstalować wymaganą bibliotekę `matplotlib`, otwórz terminal lub wiersz poleceń i wpisz:

```bash
pip install matplotlib
