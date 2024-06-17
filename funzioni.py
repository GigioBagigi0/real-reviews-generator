import re
from fuzzywuzzy import fuzz
import random
import nltk
import networkx as nx
import itertools
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import requests as rq
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor
from nltk import sent_tokenize
from nltk.corpus import stopwords
from dizt import DIZP
from collections import defaultdict
from nltk import word_tokenize
from googlesearch import search

def get_links(query, num_results=10):
    try:
        links = []
        for i, link in enumerate(search(query), start=1):
            links.append(link)
            if i >= num_results:
                break
        return links
    except Exception as e:
        print(f"An error occurred: {e}")
        return []



stop_words = set(stopwords.words('english'))


def da(output):
    d = ''
    for i in sent_tokenize(output):
        if len(i) < 300: 
            if not i in d:
                d+= i + ' '
    return d

def rimuovi_frasi(stringa): #  remove special characters to rhe prsase 
    stringa = re.sub('\(.*?\)','',stringa) # stringa = string
    stringa = re.sub('\[.*?\]','',stringa)
    stringa = re.sub('-.*?-','',stringa)
    stringa = re.sub(r"'.*?'",'',stringa)
    return stringa


# verifica_fonti = for evry phrase it find the source = check sources
def verifica_fonti(text, testo_con_rel_link):
    n_ced_list_più_link = []
    link_letter_map = {}  # Mappa per associare il link a una lettera

    for i in sent_tokenize(text):
        for tup_i in testo_con_rel_link:
            testo, url = tup_i
            cleaned_i = rimuovi_frasi(i).replace(' ', '').replace('.', '').lower()
            cleaned_testo = rimuovi_frasi(testo).replace(' ', '').replace('.', '').lower()

            if (cleaned_i in cleaned_testo) or (fuzz.ratio(cleaned_i, cleaned_testo) >= 70):
                if i.replace(' ', '') != '':
                    i = str(i) + '. '

                if url in link_letter_map:
                    link_letter = link_letter_map[url]  # Ottieni la lettera associata al link
                else:
                    link_letter = chr(len(link_letter_map) + 65)  # Genera una nuova lettera
                    link_letter_map[url] = link_letter

                n_ced_list_più_link.append((i, url, link_letter))

    return n_ced_list_più_link


HEADERS = {
    'User-Agent': ('Mozilla/5.0 (X11; Linux x86_64)'
                    'AppleWebKit/537.36 (KHTML, like Gecko)'
                    'Chrome/44.0.2403.157 Safari/537.36'),
    'Accept-Language': 'en-US, en;q=0.5'
}

def sim(text, embeddings):
    try:
        sentences = sent_tokenize(text)
        stop_words = set(stopwords.words('english'))
        clean_sentences = [" ".join([word.lower() for word in nltk.word_tokenize(sentence) if word.lower() not in stop_words]) for sentence in sentences]
        sentence_vectors = []
        
        for sentence in clean_sentences:
            words = [word for word in nltk.word_tokenize(sentence) if word in embeddings]
            if words:
                vector = np.mean([embeddings[word] for word in words], axis=0)
            else:
                vector = np.zeros(embeddings.vector_size)
            sentence_vectors.append(vector)
        
        sentence_vectors = np.asarray(sentence_vectors)
        
        if len(sentence_vectors) == 0:
            return ""
        
        similarity_matrix = cosine_similarity(sentence_vectors)
        
        relevant_sentences = []
        original_sentences = []
        
        for i, row in enumerate(similarity_matrix):
            if np.max(row) > 0.6:
                relevant_sentences.append(clean_sentences[i])
                original_sentences.append(sentences[i])
        
        if len(relevant_sentences) == 0:
            relevant_sentences = clean_sentences
            original_sentences = sentences
        
        nx_graph = nx.from_numpy_array(similarity_matrix)
        
        try:
            scores = nx.pagerank(nx_graph)
            ranked_sentences = sorted(((scores[i], sentence) for i, sentence in enumerate(relevant_sentences)), reverse=True)
        except Exception as e:
            print("Error calculating PageRank scores:", e)
            ranked_sentences = []
        
        top_sentences = list(itertools.islice(ranked_sentences, 50))  # Increase the number of selected sentences
        
        selected_original_sentences = []
        
        for _, sentence in top_sentences:
            index = clean_sentences.index(sentence)
            selected_original_sentences.append(original_sentences[index])
        
        random.shuffle(selected_original_sentences)
        out2 = " ".join(selected_original_sentences)
        
        return out2
    
    except Exception as e:
        print("Error occurred:", e)
        return ""



def algo(prod):

    testo_con_rel_link = [] # text with relative link 
    inp = prod 
    inp = f'review {inp}'


    links = get_links(inp)  

    url_content = []

    def retrieve_content(url):
        try:
            response = rq.get(url, headers=HEADERS, timeout=2)
            response.raise_for_status()  # Solleva un'eccezione se la risposta ha uno stato diverso da 200
            soup = BeautifulSoup(response.text, 'lxml')
            paragraphs = soup.find_all('p')
            text = ' '.join(p.text for p in paragraphs)
            filtered_text = rimuovi_frasi(text)
            testo_con_rel_link.append((filtered_text, url))
            return filtered_text
        except rq.exceptions.RequestException as e:
            print(f"Errore durante la richiesta a {url}: {e}")
            return ''
        except Exception as e:
            print(f"Errore sconosciuto durante la richiesta a {url}: {e}")
            return ''

    with ThreadPoolExecutor(max_workers=10) as executor:
        url_content = list(executor.map(retrieve_content, links))

    n = url_content

    text = " ".join(n)
    
    return text, links, testo_con_rel_link

def llnew(b, links):
    new_links = []
    for cef, cer, cea in b:
        for i in links:
            if i == cer:
                new_links.append((cer, cea))
    new_new_links = []
    for i in new_links:
        if i not in new_new_links:
            new_new_links.append(i)
    return new_new_links


def cercer(adv, text): 
    c = ''
    for i in sent_tokenize(text):
        common_words = set(adv.lower().split()) & set(i.lower().split())
        if len(common_words) >= 1 and i.lower() not in c.lower():
            c += i + '. '

    return c


def extract_main_topic(sentence, nlp, pr):
    pr = pr.lower()
    sentence = sentence.lower()

    for i in pr.split(' '):
        sentence = sentence.replace(i, '')

    doc = nlp(sentence)

    main_topic_tokens = []
    found_main_topic = False

    for token in doc:
        if token.pos_ in ["NOUN", "PROPN"]:
            main_topic_tokens.append(token.text)
        else:
            if main_topic_tokens:
                found_main_topic = True
                break  

    if found_main_topic:
        main_topic = " ".join(main_topic_tokens)
    else:
        main_topic = None  

    return main_topic


def group_similar_sentences(input_list, nlp, pr):
    groups = {}

    for text_tuple in input_list:
        text, label, link = text_tuple
        text = text.replace('...', '.')
        clean_text = ' '.join([token.text for token in nlp(text) if token.text.lower() not in stop_words])
        topic = extract_main_topic(clean_text, nlp, pr)

        # Check if topic is None or if it's in the product text (pr)
        if topic is not None and topic not in pr.lower():
            if topic not in groups:
                groups[topic] = []

            added_to_group = False

            for existing_text, existing_label, existing_link in groups[topic]:
                clean_existing_text = ' '.join([token.text for token in nlp(existing_text) if token.text.lower() not in stop_words])
                similarity = nlp(clean_text).similarity(nlp(clean_existing_text))

                if similarity > 0.7:
                    groups[topic].append((text, label, link))
                    added_to_group = True
                    break

            if not added_to_group:
                groups[topic].append((text, label, link))

    return groups




def trova_topic_prodotto(input_prodotto):
    if input_prodotto in DIZP:
        return DIZP[input_prodotto]
    else:
        return []
    

def trova_prodotto_e_topic(testo, dizionario):
    parole = word_tokenize(testo)  # Splitta il testo in parole
    
    occorrenze = defaultdict(int)
    
    for chiave, topic in dizionario.items():
        if isinstance(chiave, tuple):
            # Se la chiave è una tupla, conta quante parole sono presenti nel testo
            conteggio = sum(1 for parola in chiave if parola in parole)
            occorrenze[chiave] += conteggio
        else:
            occorrenze[chiave] += parole.count(chiave)
    
    # Trova il prodotto con il conteggio massimo
    prodotto_migliore = max(occorrenze, key=lambda k: (occorrenze[k], len(k) if isinstance(k, tuple) else 1))
    
    # Cerca la chiave nel dizionario come tupla
    topic_corrispondente = dizionario.get(prodotto_migliore, [])
    
    return prodotto_migliore, topic_corrispondente


def divg(topics, out):
    result = []

    # Utilizza espressioni regolari per trovare frasi
    frasi = re.findall(r'\w[^.!?]*[.!?]', out)

    for frase in frasi:
        topic_associato = None
        for topic in topics:
            if topic in frase:
                topic_associato = topic
                break

        if topic_associato is None:
            topic_associato = 'Altro'

        # Aggiungi la frase al dizionario corrispondente al topic
        found_topic = next((item for item in result if item['Topic'] == topic_associato), None)
        if found_topic:
            found_topic['Frasi'].append(frase.strip())
        else:
            result.append({'Topic': topic_associato, 'Frasi': [frase.strip()]})

    return result


def terter(out, topics):
    result = {}

    for frase, label, link in out:
        frasi = re.findall(r'\w[^.!?]*[.!?]', frase)
        topic_associato = None
        for topic in topics:
            if topic in frase:
                topic_associato = topic
                break

        if topic_associato is None:
            topic_associato = 'other'

        if topic_associato not in result:
            result[topic_associato] = []

        result[topic_associato].append(frase)

    return result



def ff(out, topics): # puts all categories in a dictionary
    topics.append('price')
    topics.append('other') 
    dic = {}

    for topic in topics:
        dic[topic] = []

    for item in out:
        frase, link, label = item
        topic_associato = None

        for topic in topics:
            if topic.lower() in frase.lower() or any(part_topic.lower() in frase.lower() for part_topic in topic.split(' ')):
                topic_associato = topic
                break
            
        if topic_associato is None:
            topic_associato = 'other'

        dic[topic_associato].append(item)

    return dic