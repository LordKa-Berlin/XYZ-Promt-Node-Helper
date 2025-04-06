

Die zielsetzung des Scripte ist folgendes: Ich möchte in der GUI von Automatic1111 oder Forge die Funktion Script XYZ Prompt ersetzen nutzen, dafür muss man in der GUI in einem Textfeld werte eintragen, (Baum, Haus,Auto,Wasser) der este Wert ist der Zeile ist der wert nach dem im Prompt gesucht wird, nach dem ersten Durchlauf tauscht Forge oder Automatic1111 im Prompt den werd Baum mit dem wert Wasser aus und führt einen neuen generierungsdurchlauf durch, mit dem wert Haus, danach folgen dann Auto und Wasser.
Mit dem Program XYZScript Liste möchte ich mir die arbeit mit dem Einfügen der Daten zum ersetzen des Promtes erleichtern, ich erstelle mir zusammen klickbare Vorlagen von Werten, die ich in die Zwischenablage kopiere und dann in die Gui von Forge oder Automatic1111 einfüge um damit verschiedene Prompts automatisch generieren zu lassen.

####################################################################################################

Hier folgt der komplette Code (Version V29), der im Anzeige‑Modus jede Zeile folgendermaßen darstellt:

Bezeichner‑Button:
• Ein einzelner Klick kopiert den Inhalt aller „aktiven“ (orange/black) Wert‑Buttons in dieser Zeile in die Zwischenablage.
• Ein Doppelklick markiert den Bezeichner und alle zugehörigen Werte für das Löschen (Farbe wird rot/weiß).

Wert‑Buttons:
• Standard (aktiv): Hintergrund orange, Schrift schwarz.
• Einzelklick: Wechselt in den „deaktivierten“ Zustand (Hintergrund grau wie Formular, Schrift hellgrau).
• Doppelklick:
  – Falls nicht bereits im Lösch‑Zustand, werden sie auf „löschmarkiert“ (rot/weiß) gesetzt.
  – Wird ein bereits löschmarkierter Button erneut doppelt angeklickt, so wechselt er zurück in den aktiven Zustand.

Beim Klick auf den Formular‑„Löschen“‑Button erscheint eine Sicherheitsabfrage, in der alle (ganz oder teilweise) markierten Einträge (bzw. deren Bezeichner bzw. die zu löschenden Werte) aufgelistet werden.
– Wird der Löschvorgang bestätigt, so werden bei vollständig markierten Zeilen der ganze Eintrag gelöscht;
– Falls nur einzelne Werte markiert sind, werden diese aus dem Prom


################################################################################
Das Script soll also als praktisches Tool dienen, um in der GUI von Automatic1111 oder Forge den "Script XYZ Prompt ersetzen" zu unterstützen. Mit klickbaren Vorlagen kannst du dann einfach Werte in die Zwischenablage kopieren und in die jeweilige GUI einfügen, um unterschiedliche Prompts automatisch generieren zu lassen. 

################################################################################