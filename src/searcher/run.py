import timeit
from operator import itemgetter
from flask import Flask, render_template, request

from tokenizer import DocProcessor
from indexer import InvertedIndex, DocList


app = Flask(__name__)

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'GET':
        return render_template('index.html')#, request=request)
    else:
        abstract = '<strong>Lorem ipsum</strong> dolor sit amet, consectetur adipiscing elit. Suspendisse vitae purus sit amet magna iaculis rhoncus. Aenean ullamcorper nibh vitae lacus commodo condimentum. Aenean ornare pharetra est id porttitor. <strong>Lorem ipsum</strong> dolor sit amet, consectetur adipiscing elit. Morbi eu ante sed arcu maximus imperdiet. Phasellus id nisl quis sem consectetur sagittis. Duis placerat nisi ut nisl condimentum ornare. Sed pulvinar arcu nisl, eu faucibus dui tincidunt aliquam. Aliquam malesuada faucibus nisl, et malesuada turpis sagittis nec. Aliquam id pretium augue.'

        start_time = timeit.default_timer()
        query = request.form['query']

        dproc = DocProcessor()
        dproc.prep_query(query)
        
        iidx = InvertedIndex(
            '/home/ubuntu/eecs767/var/wikipedia-3833/term.dct',
            '/home/ubuntu/eecs767/var/wikipedia-3833/doc.lst'
        )

        dlist = DocList(
            '/home/ubuntu/eecs767/var/wikipedia-3833/doc.lst'
        )

        results = []
        if '_enhanced' in request.form:
            rel_docs = iidx.enhanced_query(dproc.tokens)
            #ranked_docs = sorted(rel_docs, key=itemgetter('fscore'), reverse=True)
#            cos_ranked_docs = sorted(rel_docs, key=itemgetter('cos_sim'), reverse=True)
            ranked_docs = sorted(rel_docs, key=itemgetter('cos_sim', 'term_prox','i_win_loc'), reverse=True)
            for doc in ranked_docs[:10]:
                results.append({
                    'url': dlist[doc['did']]['url'],
                    'title': dlist[doc['did']]['title'],
                    'abstract': abstract,
                    'cos_sim': doc['cos_sim'],
                    'term_prox': doc['term_prox'],
                    'win_loc': int(round(1/doc['i_win_loc'])),
                    'fscore': doc['fscore']
                })
        else:
            rel_docs = iidx.query(dproc.tokens)
            ranked_docs = sorted(rel_docs.items(), key=itemgetter(1), reverse=True)

            for doc in ranked_docs[:10]:
                results.append({
                    'url': dlist[doc[0]]['url'],
                    'title': dlist[doc[0]]['title'],
                    'score': doc[1],
                    'abstract': abstract
                })

        elapsed_time = timeit.default_timer() - start_time

        return render_template('index.html', 
            #request=request,
            #tokens=dproc.tokens,
            #docs=ranked_docs[:10],
            query=query,
            results=results,
            elapsed_time=round(elapsed_time,3),
            total_docs=len(dlist)
        )

if __name__ == '__main__':
    app.run('0.0.0.0', 5000)

