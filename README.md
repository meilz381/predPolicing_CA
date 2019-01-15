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

parameter rausziehen (tagesdauer, sichtreichweite polizei/einbrecher, Betrachtungsreichweite polizeimobil, einwohner, stayparameter polizei/einbrecher, Betrachtungsreichweite einbruch)

Straßenarten, Bewegung auf Straßen, Sperrung von Straßen

performance verbesserung - auteilung in sektoren

Einbrecher aufteilen, nicht gleiche Ziele

Stadtzentrum - nähe zu zentrum bei step berechnung, berücksichtigen
-bessere Infrastruktur(straßenart)
->bessere Erreichbarkeit

hover für zellen