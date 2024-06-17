from flask import Flask, render_template, request, url_for
import gensim.downloader as api
from funzioni import da, verifica_fonti, sim, algo, llnew, cercer, group_similar_sentences, trova_prodotto_e_topic, ff
import wikipedia as wk
from dizt import DIZP
import time
import spacy
from nltk import sent_tokenize
import random

wk.set_lang('en')
nlp = spacy.load("en_core_web_md") # sm/md/lg

embeddings = api.load('glove-wiki-gigaword-50') ## also glove-wiki-gigaword-100/300

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':

        testo_con_rel_link = []         

        prodotto = request.form['titolo']
        pr = prodotto
        adv = request.form['adv']
        if adv == '':
            adv = prodotto

        try:
            introduzionewk = wk.summary(prodotto)
        except:
            introduzionewk = ''

##########################################################################
        outputb, links, testo_con_rel_link = algo(prodotto)

###########################################################################
        
        start_time = time.time()

        outputb = outputb.replace('..', '.')

        prodotto, topic = trova_prodotto_e_topic(outputb, DIZP)
        
        cet = []

        new_b = sent_tokenize(outputb)

        new_outb = []

        for i in new_b:
            if i not in new_outb:
                new_outb.append(i)

        new_bb_copy = new_outb.copy()

        for i in new_bb_copy:
            for f in topic:
                new_t = f.split(' ')
                if len(new_t) == 1:
                    if f.lower() in i.lower():
                        cet.append(i)
                        new_outb.remove(i)
                        break
                else:
                    b = False
                    for g in new_t:
                        if g.lower() in i.lower():
                            cet.append(i)
                            new_outb.remove(i)
                            b = True
                            break
                    if b:
                        break

        print(len(new_outb))
        random.shuffle(new_outb)
        outt = " ".join(new_outb)

        out2 = sim(outt, embeddings)

        

        print("--- %s seconds --- impiegati da sim" % (time.time() - start_time))

        start_time = time.time()

        if isinstance(prodotto, str):
            prodotto = prodotto.strip()


        # these out* is for filter the result
        out2 = out2.replace('\n', ' ').replace('  ', ' ')
        out3 = cercer(adv, out2)
        out4 = out3.replace(' ,', ',').replace(' ;', ';').replace(' :', ':')
        out6 = da(out4)
        out62 = " ".join(cet)

        # verifica_fonti = for evry phrase it find the source = check sources
        b = verifica_fonti(out6, testo_con_rel_link)
        fferte = verifica_fonti(out62, testo_con_rel_link)

        new_new_links = llnew(b, links) # new list of links without the link we don't use

        if adv == prodotto:
            adv = ''

        ter2 = group_similar_sentences(b, nlp, pr) 

        ter = ff(fferte, topic) # puts all categories in a dictionary

        #merges the dictionaries as all sentences were divided into two groups (those that contained a predefined topic and those that did not)
        def process_dictionary(d): 
            ter3 = {}
            
            for key, value_list in d.items():
                new_a = []
                
                for tup in value_list:
                    if isinstance(tup, tuple) and len(tup) == 3:
                        first_element = tup[0].replace('.', '')
                        new_tup = (first_element,) + tup[1:]
                        new_a.append(new_tup)
                        
                        if first_element not in ter3:
                            ter3[first_element] = None
                    else:
                        new_a.append(tup)
                
                d[key] = new_a

        process_dictionary(ter)
        process_dictionary(ter2)

        ter.update(ter2)

        tercopy = ter.copy()

        for key in tercopy.keys():
            if tercopy[key] == []:
                del ter[key]

        terall = [] 

        for key in ter.keys():
            for i in ter[key]:
                terall.append(i)
        ################################################################################################################################
        print("--- %s seconds --- impiegati dal resto" % (time.time() - start_time))
        
        combinedTestList = [] # contains all the text of each category that needs to be processed for the summary
        for i, lista in ter.items():
            stringa = ""
            for e, t, d in lista:
                stringa+= " " + e.replace("'", '"')
            combinedTestList.append(stringa)
        #################################################

        return render_template('output.html', titolo=str(out3), sources=new_new_links, pr=pr, favicon_url=url_for('static', filename='favicon.ico'), b=b, topic=adv, intro = introduzionewk, ter=ter, data_set=ter, terall = terall, style=url_for('static', filename='style.css'), script=url_for('static', filename='app.js'), ct = combinedTestList)

    return render_template('index.html', favicon_url=url_for('static', filename='favicon.ico'))



# wikipedia isn't used because it don't work well
# this code is write in italian and english