""" Main file for the execution of the information extraction. """
from extracted_information_assembler import ExtractedInformationAssembler

# Konfiguration für die URL- und Inhaltsanalyse
sitemap_url = 'https://www.eak.admin.ch/eak/de/home.sitemap.xml'
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
    "Anschluss": ["/anschluss/"],
    "Personal": ["/personal/"],
    "Externe Aufträge": ["/externe_auftraege/"],
    "Arbeiten im Ausland": ["/arbeiten_im_ausland/"],
    "Beiträge & Löhne": ["/beitraege_und_loehne/"],
    "Familienzulagen": ["/familienzulagen/"],
    "Erwerbsersatzleistungen": ["/erwerbsersatz/"],
    "connect.eak": ["/connect-eak/"],
    # Private
    "Mein AHV-Konto": ["/mein_ahv-konto/"],
    "Zivilstand": ["/zivilstand/"],
    "Kinder": ["/kinder/"],
    "Arbeit": ["/arbeit/"],
    "Arbeitsunterbruch / Keine Erwerbstätigkeit": ["/arbeitsunterbruch_keine_erwerbstaetigkeit/"],
    "Pensionierung": ["/pensionierung/"],
    "Im Ausland": ["/im_ausland/"],
    "Steuerausweis": ["/steuerausweis/"],
    # Formulare
    "Formulare": ["/formulare/"],
    # Die EAK
    "Unsere Produkte": ["/unsere-leistungen/"],
    "Porträt": ["/portrait/"],
    "Organisation": ["/organisation/"],
    "Publikationen": ["/publikationen/"],
    "Kurse und Beratung": ["/kurse-und-beratung/"],
    "Offene Stellen": ["/offene-stellen/", "offene-stellen0"],
    # Reform AHV 21
    "Reform AHV 21": ["/reform-ahv21/"],
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
    rules_for_thema_by_url=rules_for_thema_by_url,
    rules_for_content=rules_for_content,
    filter_urls_by=filter_urls_by,
    content_class=content_class
)

try:
    assembler.extract_information()
    assembler.save_to_csv('extracted_data.csv')
    print("Data extraction and CSV file creation completed.")
except Exception as e:
    print(f"An error occurred during data extraction or CSV file creation: {e}")
