import requests
from bs4 import BeautifulSoup
from celery import shared_task
import networkx as nx
from io import StringIO
from urllib.parse import urljoin

def crawl_website(url: str, max_depth: int):
    visited = set()
    graph = nx.DiGraph()

    def crawl(current_url, depth):
        if depth > max_depth or current_url in visited:
            return
        visited.add(current_url)
        graph.add_node(current_url)
        try:
            response = requests.get(current_url, timeout=5)
            soup = BeautifulSoup(response.text, "html.parser")
            for link in soup.find_all("a", href=True):
                href = link["href"]
                # Приведение относительных ссылок к абсолютному виду
                if href.startswith("/"):
                    href = urljoin(current_url, href)
                # Ограничиваем парсинг внутренними ссылками (начинающимися с базового URL)
                if not href.startswith(url):
                    continue
                graph.add_edge(current_url, href)
                crawl(href, depth + 1)
        except Exception as e:
            # Логировать ошибки можно здесь
            pass
    crawl(url, 0)
    return graph


def graph_to_graphml(graph: nx.DiGraph) -> str:
    output = StringIO()
    nx.write_graphml(graph, output)
    return output.getvalue()


# @shared_task(bind=True)
# def parse_website_task(self, url: str, max_depth: int, format: str):
#     graph = crawl_website(url, max_depth)
#     result = '-'
#     if format.lower() == "graphml":
#         result = graph_to_graphml(graph)
#     # Можно добавить поддержку других форматов
#     return result

# @celery_app.task(name="app.services.parse.parse_website_task")
# def parse_website_task(self, url: str, max_depth: int, format: str):
#     graph = crawl_website(url, max_depth)
#     result = '-'
#     if format.lower() == "graphml":
#         result = graph_to_graphml(graph)
#     # Можно добавить поддержку других форматов
#     return result