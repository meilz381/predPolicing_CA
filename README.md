# Zellulärer Automat Simulation

## Implementierung
Moore-Umgebung

Zellulärer Automat mit:
* normalem Haus mit Attributen:
	* Sicherheitsausstattung
		* Initialisierung random
		* sinkt probabilistisch
		* wird durch Einbrüche in Umgebung erhöht
	* Polizeiwachen-Entfernung
		* wird bei Initialisierung berechnet
	* Polizeiagenten-Entfernung
		* wird bei jedem Schritt aktualisiert
	* Repeat-Risiko
		* sinkt probabilistisch
		* wird durch Einbrüche in Umgebung erhöht
	* Interesse(Anreiz)
		* wird durch Einbruch gesenkt
		* steigt probabilistisch
	* Erreichbarkeit
		* wird bei Initialisierung berechnet, abhängig von Entfernung zu Straßen
* gewerblichem Gebäude
* Polizeiwache
* Straße

Agenten:
* Einbrecher 
    * Bewegung gerichtet, nach Score und Entfernung
* Polizei
    * Polizei gezielt zu Einbrüchen

Topologie(Straßen - US-Style)



## offene Features

Gesetze

Verhältnis Haus, Gewerbliches Gebäude, Polizeistationen als Konstanten

Anzahl Bewohner von Haus als zusätzliches Attribut

tag/nacht in score funktion für Unterschied gewerbliches/privates Gebäude

Anordnung der Häuser logisch - nach blocks, vorherigen block berücksichtigen

Straßenarten, Bewegung auf Straßen, Sperrung von Straßen

performance verbesserung - auteilung in sektoren

Diebe aufteilen, nicht gleiche Ziele

Stadtzentrum - nähe zu zentrum bei step berechnung, berücksichtigen
-bessere Infrastruktur(straßenart)
->bessere Erreichbarkeit

hover für zellen