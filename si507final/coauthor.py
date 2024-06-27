import networkx as nx
import matplotlib.pyplot as plt
from arxiv import Search
import json
import random

class ArticleAnalyzer:
    def __init__(self):
        """
        Initialize the ArticleAnalyzer class.
        """
        self.authors = {}

    def get_articles(self):
        """
        Get articles from the arXiv API based on the user's input category.
        The method prompts the user for a category, validates the input, and then loads a random sample of 50 articles from the corresponding JSON file.
        The loaded articles are stored in the 'authors' attribute.

        Parameters
        ----------
        None

        Returns
        -------
        dict
            A dictionary containing the authors and their information.
        """
        category = input('Enter the category of articles you would like to search for out of Physics, Mathematics, Computer Science, Quantitative Biology, Quantitative Finance, and Statistics: ').lower()
        if category not in ['physics', 'mathematics', 'computer science', 'quantitative biology', 'quantitative finance', 'statistics']:
            print('Invalid category. Please try again.')
            return

        category = category.replace(' ', '_')
        with open(f'author_data/{category}_authors.json', 'r') as f:
            all_articles = json.load(f)
        articles = dict(random.sample(list(all_articles.items()), 50))
        self.authors = articles
        return articles

class AuthorVisualizer:
    def __init__(self, authors):
        """
        Initialize the AuthorVisualizer class.
        """
        self.authors = authors

    def visualize_network(self):
        """
        Visualize the author and co-author network using a graph.

        Parameters
        ----------
        None

        Returns
        -------
        NetworkX graph visualization of the author and co-author network of the chosen category.
        """
        G = nx.Graph()
        for author, data in self.authors.items():
            for co_author in data['co_authors']:
                if not G.has_edge(author, co_author):
                    G.add_edge(author, co_author, weight=1)
                else:
                    G[author][co_author]['weight'] += 1

        edge_weights = [G[u][v]['weight'] for u, v in G.edges()]

        plt.figure(figsize=(12, 8))
        pos = nx.spring_layout(G, k=1)
        nx.draw_networkx_nodes(G, pos, node_size=1500, node_color='gray')
        nx.draw_networkx_edges(G, pos, width=edge_weights, edge_color='purple', alpha=0.5)
        nx.draw_networkx_labels(G, pos, font_size=10, font_family='sans-serif')
        plt.title('Author and Co-Author Network')
        plt.axis('off')
        plt.show()

    def visualize_pubs(self):
        """
        Visualize the number of publications for each author using a bar chart.

        Parameters
        ----------
        None

        Returns
        -------
        Bar chart visualization of the number of publications for each author of the chosen category.
        """
        author_names = [author for author in self.authors.keys()]
        num_pubs = [info['num_pubs'] for info in self.authors.values()]

        plt.figure(figsize=(12, 8))
        plt.bar(author_names, num_pubs)
        plt.title('Number of Publications for Each Author')
        plt.xlabel('Author')
        plt.ylabel('Number of Publications')
        plt.xticks([]) # orignally had plt.xticks(rotation=90) and the author names were listed, but I thought it looked messy for larger datasets
        plt.show()

    def visualize_top_authors(self, top_authors):
        """
        Visualize the top 10 authors with the most publications using a horizontal bar chart.

        Parameters
        ----------
        top_authors : list
            A list of tuples containing the author name and their information.

        Returns
        -------
        Bar chart visualization of the top 10 authors with the most publications of the chosen category.
        """
        # Ensure only top 10 authors are taken
        top_authors = top_authors[:10]

        author_names = [author for author, data in top_authors]
        num_pubs = [data['num_pubs'] for author, data in top_authors]

        plt.figure(figsize=(10, 6))
        plt.barh(author_names, num_pubs, color='skyblue')
        plt.xlabel('Number of Publications')
        plt.title('Top 10 Authors with the Most Publications')
        plt.gca().invert_yaxis()
        plt.show()

    def visualize_author_network(self, author_name):
        """
        Visualize the co-author network for a specific author using a graph.

        Parameters
        ----------
        author_name : str
            The name of the author to visualize the co-author network for.

        Returns
        -------
        NetworkX graph visualization of the co-author network for the specified author.
        """
        if author_name not in self.authors:
            print(f"No data available for author: {author_name}")
            return

        G = nx.Graph()
        for author, data in self.authors.items():
            if author == author_name:
                for co_author in data['co_authors']:
                    if not G.has_edge(author, co_author):
                        G.add_edge(author, co_author, weight=1)
                    else:
                        G[author][co_author]['weight'] += 1

        edge_weights = [G[u][v]['weight'] for u, v in G.edges()]

        plt.figure(figsize=(12, 8))
        nx.draw(G, with_labels=True, node_color='skyblue', node_size=1500, edge_color=edge_weights, width=2.0, edge_cmap=plt.cm.Blues)
        plt.show()

class AuthorComparer:
    def __init__(self, authors):
        """
        Initialize the AuthorComparer class.
        """
        self.authors = authors

    def most_influential(self):
        """
        Get the most influential authors based on the number of publications.

        Parameters
        ----------
        None

        Returns
        -------
        list
            A list of tuples containing the author name and their information.
        """
        most_influential = sorted(self.authors.items(), key=lambda x: x[1]['num_pubs'], reverse=True)
        return most_influential

    def compare_authors(self, user_author):
        """
        Compare the number of unique co-authors for the user's chosen author with the author with the most unique co-authors.

        Parameters
        ----------
        user_author : str
            The name of the author to compare the number of unique co-authors for.

        Returns
        -------
        str
            A string indicating the comparison between the user's chosen author and the author with the most unique co-authors.
        """
        most_influential_author, most_influential_author_coauthors = self.num_coauths_all()
        user_author_coauthors = self.num_coauths(user_author)

        if user_author == most_influential_author:
            return f"{user_author} is the most influential author with {most_influential_author_coauthors} unique co-authors."
        elif user_author_coauthors == most_influential_author_coauthors:
            return f"{user_author} is tied with {most_influential_author} for the most unique co-authors with {most_influential_author_coauthors}."
        else:
            return f"{user_author} has {user_author_coauthors} unique co-authors, while the author with the most unique co-authors is {most_influential_author} with {most_influential_author_coauthors}."

    def num_coauths_all(self):
        """
        Get the author with the most unique co-authors and the number of unique co-authors.

        Parameters
        ----------
        None

        Returns
        -------
        tuple
            A tuple containing the author name and the number of unique co-authors.
        """
        author_coauthors = {}
        for author, data in self.authors.items():
            author_coauthors[author] = len(data['co_authors'])

        most_influential_author = max(author_coauthors, key=author_coauthors.get)
        return most_influential_author, author_coauthors[most_influential_author]

    def num_coauths(self, target_author):
        """
        Get the number of unique co-authors for a specific author.

        Parameters
        ----------
        target_author : str
            The name of the author to get the number of unique co-authors for.

        Returns
        -------
        int
            The number of unique co-authors for the specified author.
        """
        if target_author in self.authors:
            return len(self.authors[target_author]['co_authors'])
        else:
            return 0

    def visualize_unique_coauthors(self):
        """
        Visualize the number of unique co-authors for the top 10 authors with the most publications using a horizontal bar chart.

        Parameters
        ----------
        None

        Returns
        -------
        Bar chart visualization of the number of unique co-authors for the top 10 authors with the most publications of the chosen category.
        """
        # Get a list of tuples with author names and number of unique co-authors
        author_coauthors = [(author, len(data['co_authors'])) for author, data in self.authors.items()]
        # Sort the list by number of co-authors in descending order
        author_coauthors.sort(key=lambda x: x[1], reverse=True)
        # Take the top 10 authors
        top_10_authors = author_coauthors[:10]
        # Separate the author names and number of co-authors into two lists
        author_names = [author for author, _ in top_10_authors]
        num_coauthors = [coauthors for _, coauthors in top_10_authors]
        # Create the bar chart
        plt.figure(figsize=(10, 6))
        plt.barh(author_names, num_coauthors, color='skyblue')
        plt.xlabel('Number of Unique Co-authors')
        plt.title('Top 10 Authors with the Most Unique Co-authors')
        plt.gca().invert_yaxis()
        plt.show()

    def most_common_coauthors(self):
        """
        Get the authors who have co-authored the most articles together and the number of articles they have co-authored.

        Parameters
        ----------
        None

        Returns
        -------
        tuple
            A tuple containing the pair of authors and the number of articles they have co-authored together.
        """
        coauthor_counts = {}
        for author, data in self.authors.items():
            for coauthor in data['co_authors']:
                # Ensure the pair is always in the same order
                pair = tuple(sorted((author, coauthor)))
                if pair not in coauthor_counts:
                    coauthor_counts[pair] = 1
                else:
                    coauthor_counts[pair] += 1

        # Find the pair with the most co-authorships
        most_common_pair = max(coauthor_counts, key=coauthor_counts.get)
        most_common_count = coauthor_counts[most_common_pair]

        return most_common_pair, most_common_count

def main():
    """
    Main function to run the program.
    """
    analyzer = ArticleAnalyzer()
    articles = analyzer.get_articles()

    visualizer = AuthorVisualizer(analyzer.authors)
    visualizer.visualize_network()
    visualizer.visualize_pubs()

    comparer = AuthorComparer(analyzer.authors)
    most_influential_authors = comparer.most_influential()
    # print(most_influential_authors) # removed this because it was printing into the command line and it looked messy

    visualizer.visualize_top_authors(most_influential_authors)
    comparer.visualize_unique_coauthors()

    target_author = input('Enter the name of the author you would like to see the number of unique co-authors for: ')
    user_author = target_author
    print(comparer.compare_authors(user_author))
    visualizer.visualize_author_network(user_author)

    most_common_coauthors, num_articles = comparer.most_common_coauthors()
    print(f"The authors who have co-authored the most articles together are {most_common_coauthors[0]} and {most_common_coauthors[1]}, with {num_articles} articles.")

if __name__ == "__main__":
    main()