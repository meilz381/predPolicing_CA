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
    * Randomwalk

Topologie(Straßen - US-Style)



## TODO

performance verbesserung, numpy, auteilung in sektoren, OO aufheben

anderes grafik framework -> matplotlib

Polizei gezielt zu Einbrüchen/ größte positive Änderung des Scores / Gebiet mit höchstem Score

Diebe aufteilen, nicht gleiche Ziele, bei Einbruch Konstante eintragen(2x)

Gesetze

Verhältnis Haus, Gewerbehaus als Konstanten

realistischere Straßen - idee da

Straßenarten

Tag/Nacht

Stadtzentrum - nähe zu zentrum bei step berechnung, berücksichtigen
-bessere Infrastruktur(straßenart)
->bessere Erreichbarkeit

Anordnung der Häuser logisch - nach blocks, vorherigen block berücksichtigen

hover für zellen