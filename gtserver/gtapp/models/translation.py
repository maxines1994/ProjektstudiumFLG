from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from . import GtModelBasic
from gtapp.constants.languages import *

class Translation(GtModelBasic):
    """
    Dieses Model speichert allerhand englische Strings und die entsprechende deutsche Uebersetzung.
    """

    string_en = models.CharField(max_length=128, unique=True)
    string_de = models.CharField(max_length=128, unique=True)



    def get_translation(to_language: str, translate_string: str):
        """
        Gibt die Uebersetzung des von translate_string in der Sprache to_language zurueck.

        Beispiel:      
            get_translation(LANG_EN, "Baum") 
        gibt "Tree" zurück, wenn so ein Eintrag in der Translation-Tabelle existiert.
        """

        my_translation = determine_string_of_language(to_language=to_language, translate_string=translate_string)

        if to_language == LANG_EN:
            return my_translation.string_en
        
        if to_language == LANG_DE:
            return my_translation.string_de


    def append(english_string: str, german_string: str):
        """
        Fuegt eine neue Ubersetzung fuer einen englischen/deutschen String hinzu. Dazu muss man beide Sprachversionen
        des Strings uebergeben.
        """
        Translation.objects.create(string_en=english_string, string_de=german_string)

    
    def change(to_language: str, english_string: str, german_string: str):
        """
        Aendert eine bereits bestehende Uebersetzung. to_language uebergibt die Sprachversion, die geaendert werden soll.
        Der dazugehoerige language_string wird geupdatet. Der andere String dient der Ermittlung des Datensatzes, der geupdatet werden soll.

        Beispiel: 
            Translation.change(LANG_DE, "Apple", "Apfel")

        Es wird nach dem englischen String "Apple" gesucht und die zugehoerige deutsche Uebersetzung in "Apfel" geaendert. Der englische String wird nicht geupdatet!
        """
      
        if (to_language == LANG_DE):
            translate_string = english_string

        if (to_language == LANG_EN):
            translate_string = german_string

        my_translation = determine_string_of_language(to_language=to_language, translate_string=translate_string)

        if (to_language == LANG_DE):
            my_translation.string_de = german_string
        
        if (to_language == LANG_EN):
            my_translation.string_en = english_string


def determine_string_of_language(to_language: str, translate_string: str):
    """
    Durchsucht die Translation-Tabelle nach einer Ubersetzung des uebergebenen Strings in der uebergebenen Sprache.
    """

    try:
        if (to_language == LANG_DE):
            myTrans = Translation.objects.get(string_en=translate_string)
        
        if (to_language == LANG_EN):
            myTrans = Translation.objects.get(string_de=translate_string) 

        return myTrans    

    except ObjectDoesNotExist:
        raise Exception("Translation for '" + translate_string + "' does not exist")

