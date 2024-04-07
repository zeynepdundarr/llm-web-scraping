import requests
import fitz
from google_trans_new import google_translator
from langdetect import detect, LangDetectException
from pdfminer.high_level import extract_text

translator = google_translator()

def detect_language(text):
    try:
        return detect(text)
    except LangDetectException as e:
        print(f"Language detection failed: {e}")
        return None
    

def translate_to_english(text):
    try:
        # Translate the text to English
        translated_text = translator.translate(text, lang_tgt='en')
        return translated_text
    except Exception as e:
        print(f"Translation failed: {e}")
        return text  # Return the original text if translation fails
    

def filter_pdf_links(links):
    keywords = ["finance", "financial", "financialreport"]
    european_language_codes = ["en", "fr", "de", "it", "es", "nl", "ru", "pl", "ro", "el", "hu", "sv", "pt", "da", "fi", "sk", "sl", "lt", "lv", "et"]
    filtered_pdf_links = []

    for link in links:
        if link.strip().lower().endswith('.pdf'):
            url_contains_keyword = False
            content_contains_keyword = False
            
            detected_language = detect(text)

            if detected_language == 'en':
                modified_link = link.strip().lower()
            else:
                modified_link = translate_to_english(link.strip().lower())

            # Scan URLs for keywords
            for keyword in keywords:
                if keyword in modified_link:
                    print("PDF URL contains keyword")
                    url_contains_keyword = True
                    break

            # If the URL does not contain keywords, scan the PDF content
            if not url_contains_keyword:
                text = pdf_word_scanner(link, keyword)
                if text:
                    detected_language = detect(text)

                    if detected_language == 'en':
                        print("PDF content is already in English.")
                        translated_text = text
                    elif detected_language in european_language_codes:
                        # Translate to English if the content is not in English but is a European language
                        translated_text = translate_to_english(text)
                        print("PDF content translated to English for keyword scanning.")
                    else:
                        print("PDF language is not European or detection failed.")
                        continue
                
                    # Now scan the translated text for keywords
                    for keyword in keywords:
                        if keyword in translated_text.lower():
                            print("PDF content contains keyword after translation")
                            content_contains_keyword = True
                            break

            if url_contains_keyword or content_contains_keyword:
                filtered_pdf_links.append(link)
        
    return filtered_pdf_links



def test_filter_pdf_link(link):
    keywords = ["finance", "financial", "financialreport"]
    filtered_pdf_links = []

    if link.strip().lower().endswith('.pdf'):
        url_contains_keyword = False
        content_contains_keyword = False
        
        detected_language = detect(link)

        if detected_language == 'en':
            modified_link = link.strip().lower()
        else:
            modified_link = translate_to_english(link.strip().lower())

        # Scan URLs for keywords
        for keyword in keywords:
            if keyword in modified_link:
                print("PDF URL contains keyword")
                url_contains_keyword = True
                break

        if url_contains_keyword or content_contains_keyword:
            filtered_pdf_links.append(link)
    
    return filtered_pdf_links


def test_pdf_content_link(text):
    content_contains_keyword = False
    keywords = ["finance", "financial", "financialreport"]
    european_language_codes = ["en", "fr", "de", "it", "es", "nl", "ru", "pl", "ro", "el", "hu", "sv", "pt", "da", "fi", "sk", "sl", "lt", "lv", "et"]
    filtered_pdf_links = []

    # If the URL does not contain keywords, scan the PDF content
    if text:
        detected_language = detect(text)

    if detected_language == 'en':
        print("PDF content is already in English.")
        translated_text = text
    elif detected_language in european_language_codes:
        # Translate to English if the content is not in English but is a European language
        translated_text = translate_to_english(text)
        print("PDF content translated to English for keyword scanning.")
    else:
        print("PDF language is not European or detection failed.")
 

    # Now scan the translated text for keywords
    for keyword in keywords:
        if keyword in translated_text.lower():
            print("PDF content contains keyword after translation")
            content_contains_keyword = True
    return content_contains_keyword


def pdf_word_scanner(pdf_url, keyword):
    try:
        response = requests.get(pdf_url)
        response.raise_for_status()
        
        with fitz.open(stream=response.content, filetype="pdf") as doc:
            text = ""
            for page in doc:
                text += page.get_text()
            if keyword in text.lower():
                return True
    except Exception as e:
        print(f"Failed to scan {pdf_url}: {e}")

    return False



if __name__ == "__main__":

    german_paragraph_1 = "Die finanzielle Lage des Unternehmens hat sich im letzten Quartal deutlich verbessert. Um weiterhin erfolgreich zu sein, müssen wir unsere Finanzstrategien stetig anpassen. Es ist entscheidend, dass alle Abteilungen eng zusammenarbeiten, um unsere finanziellen Ziele zu erreichen."
    german_paragraph_2 = "Der Himmel war heute Morgen außergewöhnlich klar und blau. Viele Menschen gingen im Park spazieren, um das schöne Wetter zu genießen. Es wird erwartet, dass die Temperaturen im Laufe der Woche steigen."
    french_paragraph_1 = "La situation financière de notre entreprise s'est considérablement améliorée au cours du dernier trimestre. Pour continuer à réussir, nous devons constamment adapter nos stratégies financières. Il est crucial que tous les départements travaillent en étroite collaboration pour atteindre nos objectifs financiers."
    french_paragraph_2 = "Le ciel était exceptionnellement clair et bleu ce matin. Beaucoup de gens se promenaient dans le parc pour profiter du beau temps. Les températures devraient augmenter au cours de la semaine."
    english_paragraph_1 = "The financial status of the company has significantly improved in the last quarter. To continue being successful, we must constantly adapt our financial strategies. It's critical that all departments work closely together to achieve our financial goals."
    english_paragraph_2 = "The sky was exceptionally clear and blue this morning. Many people were out walking in the park to enjoy the beautiful weather. Temperatures are expected to rise throughout the week."

    # print(test_pdf_content_link(german_paragraph_1))
    # print(test_pdf_content_link(german_paragraph_2))
    # print(test_pdf_content_link(french_paragraph_1))
    # print(test_pdf_content_link(english_paragraph_1))
    # print(test_pdf_content_link(english_paragraph_2))

    print("link: ", test_filter_pdf_link('https://example.com/de/bericht-finanziell.pdf'))
    print("link []:", test_filter_pdf_link('https://example.com/de/bericht-nokeyword.pdf'))
    print("link: ",test_filter_pdf_link('https://example.com/fr/rapport-financier.pdf'))
    print("link []:",test_filter_pdf_link('https://example.com/fr/rapport-nokeyword.pdf'))
    print("link: ",test_filter_pdf_link('https://example.com/en/report-financial.pdf'))
    print("link []:",test_filter_pdf_link('https://example.com/en/report-nokeyword.pdf'))
