data.py: 
- Speicherung aller Daten 
  - sowohl von den matplotlib 
  - als auch von Google Koords (falls die getrennt werden)
- Definieren der Rk Daten (nachdem diese augerechnet wurden im main.py Teil)

main_plt.py:
- Prolemdefinition
  - Nebenbedinungen 
  - ZF
  - Optimierung 
- Visualisierung durch Matplotlib

main_ggl.py:
- Prolemdefinition
  - Nebenbedinungen 
  - ZF
  - Optimierung 
- Visualisierung durch Fulium und Googlemaps

R_k_calc.py:
- Berechnung der R_k Werte in dieser Datei 
Werte: 



Codeausführung beim ersten Mal:
- # [carrier_1.py]: Im Code den Bereich Normal Execution auskommentieren und First Time Execution durcreadmehführen 
                    -> Skript ausführen
                    -> Carrier_1 spezifischen Durations, Kosten etc. werden berechnet und in Dateien festgehalten
- # [carrier_2.py]: Gleiches wie bei Carrier 1
- # [carrier_3.py]: Gleiches wie bei Carrier 1 & 2
                    -> Alle drei Carrierspezifischen Daten wurden berechnet 

- # [nocolab.py]:   Zunächst Carrier1 spezifischen Daten importieren und Programm ausführen (danach mit den anderen Carrier das gleiche)
                    -> Das sowohl für die live Daten als auch für die simplen Daten
                    -> R_k Werte für alle Carrier werden berechnet

- # [data.py]:      R_k Werte (sowohl live als auch simple) in data.py eintragen

- # [main.py]:      Main Funktion zunächst mit den simplen Werten und danach mit den live Werten ausfüllen und anzeigen lassen


Gedanken: 
- carrierspezifische Dateien: 
  - Exakte Unterteilung der Carrier auf die einzelnen Carrier für die Berechnung R_ks
  - alles in eine Funktion hab ich leider vom Code her nicht hinbekommen vlt. geht das ja noch aber so funktioniert es und das ist die Hauptsache 
  - falls ich noch Zeit habe versuche ich evtl hier das ganze nochmal zu optimieren

- data.py:
  - Zusammenstellungen aller relevanten Daten 
  - Wichtig für die Main.py Funktion 
  - Berechnung aller Durations sowohl simple als auch live

- main.py: 
  - Berechnung aller Werte und Optimieren 
  - Mit Valid Inequalities (beschleuningt Lösungsprozess)
  - Funktionen zum plotten sowohl plt als auch folium/google

-Warum Google Plotten: 
  - Bei einem echten Tourenplanungsproblem reichen auch nicht die euklidischen Distanzen
  - Daher hab ich eine realistische Kostenfunktion programmiert (Basierend auf diversen aspekten wie Benzinpreise, Stundenlohn des MItarbeiters etc.)
  - Diese Konstenfunktion auf die Zeit und Distanzen kalkuliert durch die Googlemaps api angewendet 
  - Und das ganze dann anhand von Folium geplottet und ausgegeben
  - Live Daten verwenden
  -> Der eigentliche Grund ist dass ich da nochmal eine draufsetzen wollte von der Seminararbeit und nochmal näher an die Realität bei der Bachelorarbeit kommen wollte



