"""
Das ist eine Liste von Allgemeinen Konstanten.
"""

"""
Unknown ist der sogenannte Minus-Eins-Datensatz. Fremdschluessel sollen nicht NULL sein, deshalb verweisen sie standardmaessig
auf einen Datensatz mit der ID = -1. Dieser hat dann die Bezeichnung "(unknown)", bzw. "(unbekannt)". Falls man in einer Tabelle
Daten aus einer Tabelle des Fremdschluessels anzeigen will, erhaelt man dann in jedem Fall einen Datensatz zurueck.
Waere der Fremdschluessel NULL koennte es bei einer Abfrage in der Datenbank knallen.
"""
UNKNOWN     = -1