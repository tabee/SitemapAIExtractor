from extracted_information_assembler import ExtractedInformationAssembler

assembler = ExtractedInformationAssembler(
    sitemap_url='https://www.eak.admin.ch/eak/de/home.sitemap.xml',
    rules_for_url={
        "Firmen": ["firmen"], 
        "Private": ["dokumentation"],
        },
    rules_for_content={
        "AHV": ["alters- und hinterlassenenvorsorge", "ahv", "1. säule"], 
        "IV": ["Invalidenversicherung", " iv", "invalid"],
        "EO": ["erwerbsausfall", "eo", "erwerbsersatz", "mutterschaft", "vaterschaft"],
        "MSE": ["mutterschaftsentschädigung", "mse"],
        "FamZG": ["Familienzulagen", "famzg", "familienzulage", "familienzulagen"],
        "EAK": ["geschäftsleitung", "eak", "jahresbericht", "andrea steiner"],
        },
    filter_str="/de/home/Firmen/arbeiten_im_ausland/",
    content_class='main-content'
)
assembler.extract_information()
assembler.save_to_csv('extracted_data.csv')
print("Data extraction and CSV file creation completed.")
