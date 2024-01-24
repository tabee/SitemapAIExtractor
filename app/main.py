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
    "EAK": ["/eak/"],
    "Publikation": ["/publikationen/"],
    "Jahresbericht": ["/jahresberichte/"],
    "News-mitteilung": ["/mitteilungs-archiv/"],
    "Neuerungen-mitteilung": ["neuerungen"],
}
rules_for_content = {
    "AHV": ["alters- und hinterlassenenvorsorge", "ahv", "1. säule"], 
    "IV": ["Invalidenversicherung", "iv", "invalid"],
    "EO": ["erwerbsausfall", "eo", "erwerbsersatz", "mutterschaft", "vaterschaft"],
    "MSE": ["mutterschaftsentschädigung", "mse"],
    "FamZG": ["Familienzulagen", "famzg", "familienzulage", "familienzulagen"],
    "EAK": ["geschäftsleitung", "eak", "jahresbericht", "andrea steiner"]
}

# Initialisierung und Ausführung des Informationssammlers
assembler = ExtractedInformationAssembler(
    sitemap_url=sitemap_url,
    rules_for_url=rules_for_url,
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
