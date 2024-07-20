import requests
from bs4 import BeautifulSoup
import networkx as nx
import matplotlib.pyplot as plt
from collections import defaultdict


cache = {}

def get_dblp_coauthors(url):
    """
    Fetch coauthor information from a given DBLP author page URL.

    Args:
        url (str): The URL of the DBLP author page.

    Returns:
        coauthors (defaultdict): A dictionary with coauthor names as keys and 
                                 the number of collaborations as values.
        url_to_name (dict): A dictionary mapping author URLs to their names.
    """
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
    """
    Get all coauthors for a list of professors.

    Args:
        professor_urls (dict): A dictionary with professor names as keys and their DBLP URLs as values.

    Returns:
        collaboration_count (defaultdict): A dictionary with (professor, coauthor) pairs as keys and 
                                           the number of collaborations as values.
        secondary_professors (dict): A dictionary with coauthor names as keys and their DBLP URLs as values.
    """
    collaboration_count = defaultdict(int)

    for professor_name, url in professor_urls.items():
        coauthors = get_dblp_coauthors(url)
        print(f"Coauthors for {professor_name}: {coauthors}")  # 调试信息
        for coauthor_name, count in coauthors.items():
            collaboration_count[(professor_name, coauthor_name)] += count

    return collaboration_count

def build_network_graph(collaboration_count, min_weight=1):
    """
    Build a network graph based on collaboration counts.

    Args:
        collaboration_count (defaultdict): A dictionary with (professor, coauthor) pairs as keys and 
                                           the number of collaborations as values.
        min_weight (int): Minimum weight of edges to be included in the graph.

    Returns:
        G (networkx.Graph): A NetworkX graph object.
    """
    G = nx.Graph()

    for (professor, coauthor), count in collaboration_count.items():
        if count >= min_weight:
            G.add_edge(professor, coauthor, weight=count)

    print(f"Nodes: {G.nodes()}")  
    print(f"Edges: {G.edges(data=True)}")  

    return G


def visualize_network(G, major_professors, filename):

    """
    Visualize the network graph and save it to a file.

    Args:
        G (networkx.Graph): A NetworkX graph object.
        major_professors (list): A list of major professor names.
        filename (str): The filename to save the visualization.
    """

    pos = nx.spring_layout(G, k=0.5, iterations=100)


    node_colors = ['skyblue'] * len(G.nodes())


    for professor in major_professors:
        node_colors[list(G.nodes()).index(professor)] = 'red'


    for professor in major_professors:
        edges = G.edges(professor, data=True)
        if edges:
            sorted_edges = sorted(edges, key=lambda x: x[2]['weight'], reverse=True)
            if len(sorted_edges) > 0:
                max_node = sorted_edges[0][1] if sorted_edges[0][0] == professor else sorted_edges[0][0]
                node_colors[list(G.nodes()).index(max_node)] = 'red'
            if len(sorted_edges) > 1:
                second_max_node = sorted_edges[1][1] if sorted_edges[1][0] == professor else sorted_edges[1][0]
                node_colors[list(G.nodes()).index(second_max_node)] = 'gold'
            if len(sorted_edges) > 2:
                third_max_node = sorted_edges[2][1] if sorted_edges[2][0] == professor else sorted_edges[2][0]
                node_colors[list(G.nodes()).index(third_max_node)] = 'pink'

    edges = G.edges(data=True)
    weights = [edge[2]['weight'] for edge in edges]

    plt.figure(figsize=(14, 14))
    nx.draw(G, pos, with_labels=True, node_size=800, node_color=node_colors, font_size=8, font_weight="bold")
    nx.draw_networkx_edge_labels(G, pos, edge_labels={(u, v): d['weight'] for u, v, d in edges}, font_size=8)
    plt.savefig(filename)
    plt.close()


if __name__ == "__main__":
    professor_urls = {
        "[ProfessorName]": "[dplp_url]",
    }
    
    major_professors = list(professor_urls.keys())
    collaboration_count = get_all_coauthors(professor_urls)
    G = build_network_graph(collaboration_count, min_weight=2) 
    

    visualize_network(G, major_professors, "full_network.png")
    
