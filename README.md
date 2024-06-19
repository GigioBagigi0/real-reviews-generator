# ARG - ALL REVIEW GENERATOR

ARG is an open-source site for generating point-based (topic) reviews for educational purposes only

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install all the necessary libraries.

```bash
pip install fuzzywuzzy nltk networkx numpy scikit-learn requests beautifulsoup4 concurrent.futures flask gensim==3.8.1 spacy wikipedia googlesearch
```
## Usage
To use the generator, you need to start the flask server with the following command:
```bash
flask run
```
you have to wait for the server to start, when it starts it will tell you what port it is open to (it should open to the link 127.0.0.1:5000), you should receive this message:
```bash 
C:\Users\yourUserName\Desktop\ARG>flask run
 * Debug mode: off
WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
 * Running on http://127.0.0.1:5000
Press CTRL+C to quit
```
than you can go to the page and see this:
![START](/START.png "")

when you have decided which product to see the review of there will be a loader, after which you will have the following screen:

![out](/out.png "")

you can summarize evry chategory (group of phrease) with the following button: 
![sum](/sum.png "")
the result is not very good but it is still a starting point

there is also the possibility to insert a custom topic which for now does not support the summary function which I will implement soon
## Conclusions
the idea itself is fantastic in my opinion but unfortunately it is not possible to take data from other sites without their consent to use them like this. It would also be nice to create a normal review site... it would be very useful but a large initial community would be needed for this reason I decided to create this project even if it is not possible to publish this site online... right now the output is not the best but it would be enough to use a more sophisticated artificial intelligence using the APIs of GPT3.5/llama/gemini etc, I decided to use transformers.js because it is a very interesting and very light project without the need for server-side artificial intelligence (not counting the models for word embeddings)

soon the code will be fully commented and translated entirely into English
## Other to know/problems
there is a possibility that you can have problems with the gensim library having problems with the collections library, just manually edit the files (they will be reported as an error) and one by one you will have to manually edit an import, if I remember there is a problem that certain things must be imported from collection and others from collection.abc so you just need to find the "right combination" it does not take much time to solve this problem and this is told to you by a programmer who when he encountered this error did not know much about it, there are also various online forums that talk about it.

for example in this file (fasttext.py) by default there would be "from collection import ..." but it doesn't work most likely because of the older version of gensim and you have to use collection.abc as in the image
![p](/colProblems.png 'p')

<span style="font-size:larger;">AS OF NOW IT IS NOT FINISHED AND ONLINE PUBLICATION IS NOT POSSIBLE AS IT DOES NOT RESPECT COPYRIGHT AND VARIOUS COPYRIGHTS SO THIS PROJECT IS ONLY AN EDUCATIONAL PURPOSE PROJECT</span>

## Contributing

FOR SUGGESTIONS/IMPROVEMENTS/COLLABORATION REQUEST GO TO THIS LINK: 

https://forms.gle/tV1i3YbnB6A9iJsT7

## License
MIT License

Copyright (c) 2024 GigioBagigi0

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
