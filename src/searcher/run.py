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
        start_time = timeit.default_timer()
        query = request.form['query']

        dproc = DocProcessor()
        dproc.prep_query(query)
        
        iidx = InvertedIndex(
            '/home/ubuntu/eecs767/var/ku/term.dct',
            '/home/ubuntu/eecs767/var/ku/doc.lst'
        )
        rel_docs = iidx.query(dproc.tokens)
        ranked_docs = sorted(rel_docs.items(), key=itemgetter(1), reverse=True)

        dlist = DocList(
            '/home/ubuntu/eecs767/var/ku/doc.lst'
        )

        abstract = 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Suspendisse vitae purus sit amet magna iaculis rhoncus. Aenean ullamcorper nibh vitae lacus commodo condimentum. Aenean ornare pharetra est id porttitor. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Morbi eu ante sed arcu maximus imperdiet. Phasellus id nisl quis sem consectetur sagittis. Duis placerat nisi ut nisl condimentum ornare. Sed pulvinar arcu nisl, eu faucibus dui tincidunt aliquam. Aliquam malesuada faucibus nisl, et malesuada turpis sagittis nec. Aliquam id pretium augue.'

        results = {}
        for doc in ranked_docs[:10]:
            results[doc[0]] = {
                'url': dlist[doc[0]],
                'score': doc[1],
                'abstract': abstract
            }

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

