from flask import Flask, url_for, request, render_template, redirect, session, jsonify
from py2neo import Graph, Node, Relationship

graph = None
recently = []

app = Flask(__name__)

@app.route('/')
def index():
    return render_template(u'index.html')

@app.route('/_get_entry')
def get_entry():
    #lemma = request.args.get('lemma', u'', type=unicode).replace(u"'", u'')
    #trans = request.args.get('trans', u'', type=unicode)
    #entry = find_entry(req, trans)
    #return jsonify(entryHtml=entry)
    pass

@app.route('/handler/', methods=['GET'])
def handler():
    htmls = ''
    req = request.args.get('word')
    results = search_graph(req)

    n = 5
    recentlyHtml = ''

    if len(recently) < n:
        recently.append(req)
    else:
        recently.remove(recently[0])
        recently.append(req)

    for word in recently:
        recentlyHtml += '<p>' + word + '</p>'

    for i in range(len(results)):
        htmlString = '<p><a href="javascript:void(0);" id="info">' + str(i+1) + '</a>. ' + results[i] + '</p>'
        htmls += htmlString

    return jsonify(entries = htmls, recently = recentlyHtml)



def load_graph(graph_url):
    global graph
    graph = Graph(graph_url)

def search_graph(word):
    results = []
    graph_results = graph.cypher.execute("MATCH (a)-[r]->(b) WHERE a.word = '" + word +  "' OR b.word = '" + word +  "' RETURN a,b")
    for res in graph_results:
        results.append(res.a['word'] + ' ' + res.b['word'])
    return results

def start_server():
   load_graph('http://rhymes:Zfye6tlzvOHly2eCq70t@rhymes.sb05.stations.graphenedb.com:24789/db/data/')
   app.run(port=2020)

if __name__ == u'__main__':
    start_server()