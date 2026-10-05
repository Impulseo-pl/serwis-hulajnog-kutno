# Serwis hulajnóg Kutno – demo (Ksawery)

Lead z CRM: Ksawery, „Serwis Hulajnogi Kutno”, 889 503 420, Revoltec@vp.pl. Demo: https://impulseo-pl.github.io/serwis-hulajnog-kutno/ (sprawdzamy **zawsze z `?team=1`**).
Jego obecna strona naprawa-hulajnogi.eu pokazuje błąd WordPressa (Fatal error) – stan z 05.10.2026.

Źródła treści: wizytówka Google (adres, godziny, 4,4 / 10 opinii, opinie), ogłoszenie tablica.com 277633 (zakres usług, odbiór do 30 km), post FB „Hulajnogi Serwis Naprawa” z 17.09, Złota Firma (opinie Julek O., Klaudia B.).
Zdjęcie: jedyne własne z wizytówki (skuter). Cen klient nie podał – na stronie brak kwot.

Wzór: Volt Garage (formularz w krokach, usługi jak cennik, FAQ, obszar) + GRENZ (szybki kontakt). Kolor: żółty sygnałowy na grafitowym, Barlow Semi Condensed + Barlow.
Rysunek hulajnogi w SVG = wybór usterki; strefa odbioru liczona haversine z `assets/miejscowosci.json` (Nominatim).
Zrzuty: `python _src/shots.py 1440` (serwer z `C:\Users\kluch`: `python -m http.server 8124`).
