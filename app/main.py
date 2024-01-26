""" Main file for the execution of the information extraction. """
from extracted_information_assembler import ExtractedInformationAssembler
import toml

# Laden der Konfigurationsdatei
config = toml.load("config_eak.toml")

# Zugriff auf die Konfigurationswerte
sitemap_url = config["Sitemap"]["url"]
sitemap_url_k = config["Sitemap"]["k"]
filter_urls_by = "/de/"
content_class = 'main-content'
# Regeln für URL- und Inhaltsanalyse
rules_for_url = {
    "Firmen": ["/firmen/"], 
    "Private": ["/dokumentation/"],
    "Publikation": ["/publikationen/"],
    "Jahresbericht": ["/jahresberichte/"],
    "News-mitteilung": ["/mitteilungs-archiv/"],
    "Neuerungen-mitteilung": ["neuerungen"],
}
rules_for_thema_by_url = {
    # Firmen
    "Anschluss": ["/anschluss/", "anschluss.html"],
    "Personal": ["/personal/", "personal.html"],
    "Externe Aufträge": ["/externe_auftraege/", "externe_auftraege.html"],
    "Arbeiten im Ausland": ["/arbeiten_im_ausland/", "arbeiten_im_ausland.html"],
    "Beiträge & Löhne": ["/beitraege_und_loehne/", "beitraege_und_loehne.html"],
    "Familienzulagen": ["/familienzulagen/", "familienzulagen.html"],
    "Erwerbsersatzleistungen": ["/erwerbsersatz/", "erwerbsersatz.html"],
    "connect.eak": ["/connect-eak/", "connect-eak.html"],
    # Private
    "Mein AHV-Konto": ["/mein_ahv-konto/", "mein_ahv-konto.html"],
    "Zivilstand": ["/zivilstand/", "zivilstand.html"],
    "Kinder": ["/kinder/", "kinder.html"],
    "Arbeit": ["/arbeit/", "arbeit.html"],
    "Arbeitsunterbruch / Keine Erwerbstätigkeit": ["/arbeitsunterbruch_keine_erwerbstaetigkeit/", "arbeitsunterbruch_keine_erwerbstaetigkeit.html"],
    "Pensionierung": ["/pensionierung/", "pensionierung.html"],
    "Im Ausland": ["/im_ausland/", "im_ausland.html"],
    "Steuerausweis": ["/steuerausweis/", "steuerausweis.html"],
    # Formulare
    "Formulare": ["/formulare/", "formulare.html"],
    # Die EAK
    "Unsere Produkte": ["/unsere-leistungen/", "unsere-leistungen.html"],
    "Porträt": ["/portrait/", "portrait.html"],
    "Organisation": ["/organisation/", "organisation.html"],
    "Publikationen": ["/publikationen/", "publikationen.html"],
    "Kurse und Beratung": ["/kurse-und-beratung/", "kurse-und-beratung.html"],
    "Offene Stellen": ["/offene-stellen/", "offene-stellen0", "offene-stellen0.html"],
    # Reform AHV 21
    "Reform AHV 21": ["/reform-ahv21/", "reform-ahv21.html"],
}
rules_for_content = {
    "AHV": [
        "alters- und hinterlassenenvorsorge", 
        "alters- und hinterlassenenversicherung", 
        "ahv",
        "altersvorsorge",
        "altersrente",
        "stabilsierung der ahv",
        "ahv 21",
        "ahv21",
        "hinterlassenenrenten",
        ], 
    "IV": [
        "Invalidenversicherung", 
        " iv ", 
        "invalid", 
        "invalidenvorsorge",
        "eingliederungsmassnahmen",
        "invalidenrenten",
        "assistenzbeitrag",
        ],
    "EL": [
        "hilflosenentschädigung",
        "ergänzungsleistungen",
        "jährliche ergänzungsleistungen",
        "krankheits- und behinderungskosten",
        "recht auf ergänzungsleistungen",
        "berechnung ergänzungsleistungen",
        " el ", 
        "ergänzungsleistung",
        "minimalen Lebenskosten nicht decken",
        ],
    "EO-MSE-EAE-BUE-AdopE": [
        "erwerbsersatz", 
        "mutterschaft",
        "mutterschaftsentschädigung",
        "vaterschafts", 
        "mutter- & andern elternteil", 
        "betreuung", 
        "adoption", 
        " eo ", 
        " mse ", 
        " eae ", 
        " bue ", 
        "adope", 
        "erwerbsausfall", 
        "erwerbsersatzordnung", 
        "dienstpflicht", 
        "anderen elternteil",
        "beeinträchtigten kind",
        "beeinträchtigtes kind",
        "dienstreisende",
        ],
    "FamZG": [
        "Familienzulagen", 
        "famzg", 
        " fz ",
        "unterhalt ihrer kinder",
        "unterhalt der kinder",
        "kinder- und ausbildungszulagen",
        "kinderzulagen",
        "ausbildungszulagen",
        "familienausgleichskasse",
        "familienzulage",
        ],
}

# Initialisierung und Ausführung des Informationssammlers
assembler = ExtractedInformationAssembler(
    sitemap_url=sitemap_url,
    rules_for_url=rules_for_url,
    sitemap_url_k=sitemap_url_k,
    rules_for_thema_by_url=rules_for_thema_by_url,
    rules_for_content=rules_for_content,
    filter_urls_by=filter_urls_by,
    content_class=content_class
)

try:
    assembler.extract_information()
    assembler.do_we_have_dublicates()
    assembler.save_to_csv('extracted_data.csv')
    print("Data extraction and CSV file creation completed.")
except Exception as e:
    print(f"An error occurred during data extraction or CSV file creation: {e}")
