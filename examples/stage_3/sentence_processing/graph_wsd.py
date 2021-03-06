from nltk.corpus import wordnet as wn


class Graph:
    def __init__(self):
        self.edges = {}
        self.leng = {}
        self.num = {}

    def add_vertex(self, word):
        if word not in self.edges:
            self.edges[word] = set()

    def add_edge(self, word1, word2):
        self.edges[word1].add(word2)
        self.edges[word2].add(word1)

    def count_len(self):
        for vertex in self.edges.keys():
            self.leng[vertex] = len(self.edges[vertex])

    def count_num(self, lst):
        for number, vertex in enumerate(lst):
            self.num[vertex] = number


def get_similar(synset):
    similar_words = set()
    similar_words.update(synset.member_holonyms())
    similar_words.update(synset.member_meronyms())
    similar_words.update(synset.hypernyms())
    similar_words.update(synset.hyponyms())
    similar_words.update(synset.part_holonyms())
    similar_words.update(synset.part_meronyms())
    return(similar_words)


def add_similar(graph, synset, depth=0):
    for word in get_similar(synset):
        graph.add_vertex(word)
        graph.add_edge(synset, word)
        if depth < 3:
            add_similar(graph, word, depth+1)


def build_word_graph(lemmas_set, start_word):
    graph = Graph()
    for word_lemma, word_pos in lemmas_set:
        start_words = wn.synsets(word_lemma, pos=word_pos)
        graph.add_vertex(start_words[0])
        for word in start_words:
            # if word == start_words[0]:
            #     continue
            graph.add_vertex(word)
            graph.add_edge(start_words[0], word)
            add_similar(graph, word)
    return graph


def get_top_synsets(graph, start_word, number=3):
    graph.count_len()
    graph_vertexes = list(graph.edges.keys())
    graph.count_num(graph_vertexes)
    N = len(graph.edges)
    # print(N)
    pagerank = [1/N for i in range(N)]

    for _ in range(20):
        for i, vertex in enumerate(graph_vertexes):
            pagerank[i] = 0.85/N + 0.15*sum([pagerank[graph.num[j]] /
                                             graph.leng[j] for j in graph.edges[vertex]])

    possible_explanation = []
    for i in range(N):
        if graph_vertexes[i] in wn.synsets(start_word[0], start_word[1]):
            possible_explanation.append((pagerank[i], graph_vertexes[i]))
    return list(map(lambda x: x[1], sorted(possible_explanation)[:number]))
