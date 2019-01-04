# Zellulärer Automat Simulation

## Features
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
** Bewegung gerichtet, nach Score und Entfernung
* Polizei
** Randomwalk

Topologie(Straßen - US-Style)



## TODO

anderes grafik framework -> matplotlib
Bilder als Video / 3D Plot
Heatmap des Scores
hover für zellen

performance verbesserung

Polizei gezielt zu Einbrüchen
Diebe aufteilen, nicht gleiche Ziele

Gesetze

Verhältnis Haus, Gewerbehaus als Konstanten

realistischere Straßen - idee da
Straßenarten

Tag/Nacht

Stadtzentrum - idee(nähe zu zentrum bei step berechnung, berücksichtigen)
-bessere Infrastruktur(straßenart)
->bessere Erreichbarkeit

Anordnung der Häuser logisch - idee(nach blocks, vorherigen block berücksichtigen)
