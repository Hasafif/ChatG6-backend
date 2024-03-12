from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from tenacity import retry, stop_after_attempt, wait_exponential
import arxiv
from ath.info import *

OpenAI_key = open_ai_key
llm = ChatOpenAI(model='gpt-4', api_key=OpenAI_key,temperature=0)
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are world class technical documentation writer and an expert researcher."),
    ("user", "{input}")
])
chain = prompt | llm 
##backoff & retry implementation for gpt requests
def generate(topic,references,outline):
    if (outline != ''):
         o = chain.invoke({"input": f"generate a well structered scientific article about {topic}.Use the following outline {outline}.Use the following refernces {references}.Add in-text numeric citations with a complete references list"})
         print(o.content)
    else:
         o = chain.invoke({"input": f"generate a well structered scientific article about {topic}.Use the following refernces {references}.Add in-text numeric citations with a complete references list"})
         print(o.content)
    return o.content
def outline(topic,references):
    refs = []
    if (len(references)==0):
        arxiv = True
        for r in search_in_arxiv(topic):
            auth = []
            if (len(r.authors)==1):
                     auth.append(str(r.authors[0]))
            else:
                    for i in r.authors:
                             auth.append(str(i))
            ref = []
            ref.append(r.title)
            ref.append(r.summary)
            ref.append(str(auth))
            ref.append(parse_year(r.published))
            ref.append(r.pdf_url)
            refs.append(ref)
    else:
          arxiv = False
          refs = organize(references)
          #print(refs)
    ser = []
    for i in refs:
         #print(i)
         ser.append('\n'.join(i))
    #print(ser)
    if len(ser) > 12:
          ser = ser[:12]
    der = '\n\n\n'.join(ser)
    
    print(der)
    print(len(ser))
    o = chain.invoke({"input": f"generate a simple outline for a scientific article about {topic}.Use the following references \n {str(der)}."})
    print(o.content)
    return {'outline':o.content,'references':references,'arxiv':arxiv}
def parse_year(d) -> int:
  d = str(d)
  return d.split()[0][0:4]

##backoff & retry implementation for arxiv requests
@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
def search_in_arxiv(query: str, max_results: int = 10):
    client = arxiv.Client(page_size=100, delay_seconds=1.0, num_retries=10)
    search = arxiv.Search(
        query=query,
        max_results=max_results,
        sort_by=arxiv.SortCriterion.Relevance,
        sort_order=arxiv.SortOrder.Descending,
    )

    all_results = list(client.results(search))
    return all_results

def organize(papers):
     refs = []
     for p in papers:
        #print(p)
        try:
           auth = []
           if (len(p['authors'])==1):
                auth.append(str(p['authors'][0]))
           else:
                for i in p['authors']:
                        auth.append(str(i))
           ref = []
           ref.append(p['title'])
           ref.append(p['abstract'])
           ref.append(str(auth))
           ref.append(parse_year(p['published']))
           ref.append(p['pdf_url'])
           refs.append(ref)
        except:
             continue
     return refs
def organize_arxiv(references):
       refs = []
       for r in references:
                   auth = []
                   if (len(r.authors)==1):
                         auth.append(str(r.authors[0]))
                   else:
                      for i in r.authors:
                                 auth.append(str(i))
                   ref = []
                   ref.append(r.title)
                   ref.append(r.summary)
                   ref.append(str(auth))
                   ref.append(parse_year(r.published))
                   ref.append(r.pdf_url)
                   refs.append(ref)
       return refs
class article:
    def __init__(self,title,res,outline,arxiv):
       self.title = title
       self.papers = res
       self.outline = outline
       self.arxiv = arxiv
       self.references = self.search()
       self.article = self.generate_article()
       self.final_article = self.clean()
    def search(self):
        refs = []
        if (len(self.papers)==0):
               references = search_in_arxiv(self.title)
               refs = organize_arxiv(references)
        elif (self.arxiv):
             refs = organize_arxiv(self.papers)
        else:   
              refs = organize(self.papers)     
        ser = []
        for i in refs:
             ser.append('\n'.join(i))
        if (len(ser)>12):
             ser = ser[:12]
        der = '\n\n\n'.join(ser)
        return der
    def generate_article(self):
       out = generate(self.title,self.references,self.outline)
       return out
    def clean(self):
       out = self.article.replace('^', '').replace('#','').replace('*','')
       return out
#article("football matches prediction using AI")
#m = article("organic chemistry")
#print (m.final_article)
