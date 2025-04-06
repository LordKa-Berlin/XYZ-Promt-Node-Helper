
mache aus jedem Wert in der Ansicht liste einen anklickbaren button default Hintergrund orange, schriftfarbe schwarz = der Button ist aktiviert,

1 mal auf den Button klicken - der Button wird deaktiviert, die farbe des Buttons ändert sich: Hintergrundfarbe grau wie der Hintergrund des formulars schriftfarbe hellgrau
2. mal auf den button klicken (doppelklick) - der Button wird zum löschen markiert - die farbe des hintergrundes ändert sich auf rot, die schriftfarbe des buttons wird weiß, wenn man im Formular auf den Button löschen klickt, wird zuerst eine sicherheitsabfrage angezeigt die alle zum löschen markierten werte anzeigt und fragt ob man die wirklich löschen will. (ja/nein/abbrechen), der zeilenumbruch nach 130 Zeichen muss erhalten bleiben!

So hatte ich das nicht gemeint!
In der Ansicht Listendarstellung:
1. der Bezeichner bleibt ein eigener Button, mit der folgenden Funktion, wird er angeklickt, dann kopiert er alle aktiven Buttons aus der Zeile

2. jeder wert aus einer Zeile (zb. Bezeichner "natur" Wert Baum, wasser, heißes Feuer, erde usw.) wird als anklickbarer Buton dargestellt
default Hintergrund orange, schriftfarbe schwarz = der Button ist "aktiviert",
Mit folgender Funktionalität:

1 mal auf den Button klicken - der Button wird deaktiviert, die farbe des Buttons ändert sich: Hintergrundfarbe grau wie der Hintergrund des formulars schriftfarbe hellgrau
2. mal auf den button klicken (doppelklick) - der Button wird zum löschen markiert - die farbe des hintergrundes ändert sich auf rot, die schriftfarbe des buttons wird weiß, wenn man im Formular auf den Button löschen klickt, wird zuerst eine sicherheitsabfrage angezeigt die alle zum löschen markierten werte anzeigt und fragt ob man die wirklich löschen will. (ja/nein/abbrechen), der zeilenumbruch nach 130 Zeichen muss erhalten bleiben!

wiederholter Doppelklick, der Button wird wieder aktiviert (Orange/schwarz)

Wenn ich auf den Bezeichner klicke:
1 mal klicken, der inhalt der aktiven Buttons (orange/schwarz) wird in die zwischenablage kopiert, der inhalt der dektivierten Buttons wird nicht kopiert!
Doppelklick auf den Bezeichner:
Der bezeichner und alle Werte (Buttons) in der Zeile werden zum löschen markiert.


Die zielsetzung des Scripte ist folgendes: Ich möchte in der GUI von Automatic1111 oder Forge die Funktion Script XYZ Prompt ersetzen nutzen, dafür muss man in der GUI in einem Textfeld werte eintragen, (Baum, Haus,Auto,Wasser) der este Wert ist der Zeile ist der wert nach dem im Prompt gesucht wird, nach dem ersten Durchlauf tauscht Forge oder Automatic1111 im Prompt den werd Baum mit dem wert Wasser aus und führt einen neuen generierungsdurchlauf durch, mit dem wert Haus, danach folgen dann Auto und Wasser.
Mit dem Program XYZScript Liste möchte ich mir die arbeit mit dem Einfügen der Daten zum ersetzen des Promtes erleichtern, ich erstelle mir zusammen klickbare Vorlagen von Werten, die ich in die Zwischenablage kopiere und dann in die Gui von Forge oder Automatic1111 einfüge um damit verschiedene Prompts automatisch generieren zu lassen.

Du hast mich falsch verstanden! Der Bezeichner Button soll in der "Ansicht Liste" grau orange sein, nicht in der Bearbeiten Liste! in der Bearbeiten Liste soll er schwarz orange sein, so wie die anderen felder in der liste auch.

In der Ansicht liste kenzeichnet man den Bezeichner Button mit einem Doppelklick zum löschen der Zeile (rot/weiß) das funktioniert auch gut, ein wiederholter Doppelklick soll den Bezeichner aber wieder auf Normal setzen(grau/orange) und die werte in der Zeile des bezeicners auch wieder auf aktiv (orange/schwarz) setzen

Baue einen neuen Button ein. setze ihn rechts neben das optionsfeld Bearbeiten. Der Button soll ein Umschalter sein, zwischen "alle Werte aktiviert" (orange/schwarz), "alle Werte deaktiviert (grau/hellgrau). Der name des Buttons soll sich nach dem jweiligen zusatnd ändern. Sind alle werte aktiviert ist der Name "alle deaktivieren" sind alle werte deaktiviert, soll der name wechseln auf "alle aktivieren"

passe bitte folgendes im Script an:
1. Jetziger zustand:
1 mal auf den Button klicken - der Button wird deaktiviert, die farbe des Buttons ändert sich: Hintergrundfarbe grau wie der Hintergrund des formulars schriftfarbe hellgrau
2. mal auf den button klicken (doppelklick) - der Button wird zum löschen markiert - die farbe des hintergrundes ändert sich auf rot, die schriftfarbe des buttons wird weiß, wenn man im Formular auf den Button löschen klickt, wird zuerst eine sicherheitsabfrage angezeigt die alle zum löschen markierten werte anzeigt und fragt ob man die wirklich löschen will. (ja/nein/abbrechen), der zeilenumbruch nach 130 Zeichen muss erhalten bleiben!

wiederholter Doppelklick, der Button wird wieder aktiviert (Orange/schwarz)

Das funktioniert, lass das so!
Füge die Funktion hinzu
1 mal auf den Button klicken - der Button wird deaktiviert, die farbe des Buttons ändert sich: Hintergrundfarbe grau wie der Hintergrund des formulars schriftfarbe hellgrau - wiederholtes 1 mal klicken, button wird wieder aktiviert (orange/schwarz)

2. ändere die Optionsfelder Anzeige - Bearbeiten zu einem Toggle Button Anzeige/Bearbeiten, die Funktionalität soll dabei erhalten bleiben!


1. lösche den Copy-Master Button!
2. baue eine Backup funktion der XYPScriptPromptListe.json Datei ein. Erstelle einen Unterorder "backup-XYPScriptPromptListe", lege vor jeder änderung(vor jedem speichern) eine Sicherungskopie der Datei XYPScriptPromptListe.json in das backupverzeichnis, mit dem namen XYPScriptPromptListe.json-[Datum]-[Uhrzeit]. baue eine Funktion ein die backupdateien die älter als 30 tage sind automatisch löscht, die neusten 10 Backupdateien (nach aktuellem Datum) dürfen nicht gelöscht werden. Zeige im Statusfeld an das ein Backup erstellt wurde.
3, baue eine Importfunktion ein. erstelle einen Button an der Stelle wo der Master-Copy Button war, wenn man auf den Button klickt öffnet sich ein neues Fenster mit einem Button Import und einer auswahl funktion, mit der man die zu importierende csv Liste auswählen kann. CSV Liste, Beispiel Syntax beim import.

HairColor,blonde hair,brown hair,black hair,red hair,white hair,pink hair
Pose,standing,sitting,lying,kneeling,cross-legged,leaning
OutfitType,latex suit,lace dress,leather jacket,denim overalls,silk robe
Lighting,soft light,hard light,backlight,spotlight,side light,volumetric light
Background,forest path,urban rooftop,office room,castle hall,flower garden

verhindere doppelte Einträge
4. folgende änderung im Script ist gewünscht. verhindere das es doppelte bezeichner gibt, wird ein doppelter wert beim eingeben oder import erkannt bringe einen hinweis im status

Ersetze den Eingegebenen bezeichner durch folgende Logik: syntax -[fortlaufende Zahl] Beispiel Bezeichner Natur, der user gibt Natur ein, prüfen - gibt es schon, ersetze Natur durch Natur-1. der user gibt wieder Natur ein, Prüfe auf natur, gibt es schon, prüfe ob natur-1 schon existiert, wenn nicht ersetze durch natur-1, wenn ja dann ersetze durch natur-2 usw.

wende die selbe logik auch beim import von csv listen an

Integriere folgende Funktion:
positioniere links neben dem Import CSV Button zwei Optionsfelder
name des ersten feldes
"Output 1 comma separated
(e.g. Forge & Automatic1111)"
name des zweiten feldes:
"Output 2 Line by line
(e.g. für ComfyUI-kompatible Nodes)"
Den zeilenumbruch für den Namen des Optionsfeldes unbedingt übernehmen im code

wenn das Output 1 Feld aktiviert ist, bleibt die ausgabe in der zwischenablage so wie sie ist
wenn das Output 2 Feld aktiviert wird dann musst du die Ausgabe umformatieren. Jeder wert muss in einer eigenen zeile bereitgestellt werden, das komma wird entfernt.
Zeige oben in der Statusleiste in einem eigenem feld an, welcher Modus gerade aktiviert ist, ergänze auch die Statusmeldungen mit der info in welchem Modus die ausgabe erfolgt ist