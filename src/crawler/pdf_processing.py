import requests
import fitz
from langdetect import detect, LangDetectException
from translator import TranslationDict

def detect_language(text):
    try:
        return detect(text)
    except LangDetectException as e:
        print(f"Language detection failed: {e}")
        return None   

def filter_pdf_links(links):
    translation_dict = TranslationDict()
    translated_keywords = translation_dict.translated_keywords
    
    filtered_pdf_links = []

    for link in links:
        if link.strip().lower().endswith('.pdf'):
            url_contains_keyword = False            
            detected_language = detect(link)

            # Scan URLs for keywords
            for keyword in translated_keywords.get(detected_language, []):
                if keyword in link:
                    print("Text contains translated keyword:", keyword)
                    url_contains_keyword = True
                    break

            # If the URL does not contain keywords, scan the PDF content
            if not url_contains_keyword:
                text = pdf_word_scanner(link, keyword)
                if text:
                    detected_language = detect(text)
                
                    # Now scan the translated text for keywords
                    for keyword in translated_keywords.get(detected_language, []):
                        if keyword in text.lower():
                            print("PDF content contains keyword after translation")
                            content_contains_keyword = True
                            break

            if url_contains_keyword:
                filtered_pdf_links.append(link)
        
    return filtered_pdf_links

def test_pdf_content_link(text):
    translation_dict = TranslationDict()
    translated_keywords = translation_dict.translated_keywords
    
    content_contains_keyword = False

    if text:
        detected_language = detect(text)
    
        # Now scan the translated text for keywords
        for keyword in translated_keywords.get(detected_language, []):
            if keyword in text.lower():
                print("PDF content contains keyword after translation")
                content_contains_keyword = True
                break

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

    # print("True", test_pdf_content_link(german_paragraph_1))
    # print("False", test_pdf_content_link(german_paragraph_2))
    # print("True", test_pdf_content_link(french_paragraph_1))
    # print("False", test_pdf_content_link(english_paragraph_2))
    # print("True", test_pdf_content_link(english_paragraph_1))
    # print("False", test_pdf_content_link(english_paragraph_2))

    print("link: ", filter_pdf_links(['https://example.com/de/bericht-finanziell.pdf']))
    print("link []:", filter_pdf_links(['https://example.com/de/bericht-nokeyword.pdf']))
    print("link: ", filter_pdf_links(['https://example.com/fr/rapport-financier.pdf']))
    print("link []:", filter_pdf_links(['https://example.com/fr/rapport-nokeyword.pdf']))
    print("link: ", filter_pdf_links(['https://example.com/en/report-financial.pdf']))
    print("link []:", filter_pdf_links(['https://example.com/en/report-nokeyword.pdf']))
