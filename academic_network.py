import json
import requests
from bs4 import BeautifulSoup
import networkx as nx
import matplotlib.pyplot as plt
from collections import defaultdict

cache = {}

def get_dblp_coauthors(url):
    if url in cache:
        return cache[url]
    
    response = requests.get(url)
    
    if response.status_code != 200:
        print(f"Failed to fetch data from {url}, status code: {response.status_code}")
        return []

    soup = BeautifulSoup(response.content, 'html.parser')
    coauthors = defaultdict(int)

    section = soup.find('header', id='the2020s')
    if section:
        publications = section.find_next('ul', class_='publ-list')
        if publications:
            items = publications.find_all('li', class_='entry')
            for pub in items:
                authors = pub.select('span[itemprop="author"] span[itemprop="name"]')
                author_names = [author.text for author in authors]
                if len(author_names) > 1:
                    for author in author_names:
                        if author != url:
                            coauthors[author] += 1

    cache[url] = coauthors
    return coauthors

def get_all_coauthors(professor_urls):
    collaboration_count = defaultdict(int)
    for professor_name, url in professor_urls.items():
        coauthors = get_dblp_coauthors(url)
        print(f"Coauthors for {professor_name}: {coauthors}")  # 调试信息
        for coauthor_name, count in coauthors.items():
            collaboration_count[(professor_name, coauthor_name)] += count
    return collaboration_count

def build_network_graph(collaboration_count, min_weight=1):
    G = nx.Graph()
    for (professor, coauthor), count in collaboration_count.items():
        if count >= min_weight:
            G.add_edge(professor, coauthor, weight=count)
    print(f"Nodes: {G.nodes()}")  
    print(f"Edges: {G.edges(data=True)}")  
    return G

def export_network_data(G, filename):
    data = {
        'nodes': [{'data': {'id': node, 'label': node}} for node in G.nodes()],
        'edges': [{'data': {'source': u, 'target': v, 'weight': d['weight']}} for u, v, d in G.edges(data=True)]
    }
    with open(filename, 'w') as f:
        json.dump(data, f, indent=2)

if __name__ == "__main__":
    professor_urls = {
    }
    
    major_professors = list(professor_urls.keys())
    collaboration_count = get_all_coauthors(professor_urls)
    G = build_network_graph(collaboration_count, min_weight=1) 
    export_network_data(G, 'network_data.json')

