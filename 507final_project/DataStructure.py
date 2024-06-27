import networkx as nx
import matplotlib.pyplot as plt
from arxiv import Search
import json

class ArticleAnalyzer:

    def get_articles(self, category):
        """
        Get 300 articles from arXiv API for a given category.

        Parameters
        ----------
        category : str
            The category of articles to be retrieved.

        Returns
        -------
        list
            List of articles retrieved from the API.
        """
        query = Search(query=category, max_results=300) # cat:stat.ML, Physics, Mathematics, Computer Science, Quantitative Biology, Quantitative Finance, and Statistics.
        articles = query.results()
        return articles

    def extract_authors(self, articles, category):
        """
        Extract authors from a list of articles and save the data to a JSON file.

        Parameters
        ----------
        articles : list
            List of articles to extract authors from.
        category : str
            The category of the articles.

        Returns
        -------
        dict
            A dictionary mapping author names to a list of their co-authors.
        """
        authors = {}
        for article in articles:
            authors_list = article.authors
            for author in authors_list:
                author_name = author.name
                co_authors = [a.name for a in authors_list if a != author]
                if author_name not in authors:
                    authors[author_name] = {'co_authors': list(co_authors), 'num_pubs': 1}
                else:
                    authors[author_name]['co_authors'].extend(co_authors)
                    authors[author_name]['co_authors'] = list(set(authors[author_name]['co_authors']))
                    authors[author_name]['num_pubs'] += 1

        category = category.replace(' ', '_')

        with open(f'author_data/{category}_authors.json', 'w') as f:
            json.dump(authors, f, indent=4)

if __name__ == "__main__":
    analyzer = ArticleAnalyzer()
    categories = ['physics', 'mathematics', 'computer science', 'quantitative biology', 'quantitative finance', 'statistics']
    for category in categories:
        articles = analyzer.get_articles(category)
        analyzer.extract_authors(articles, category)
        print(f'Authors extracted for {category} category.')