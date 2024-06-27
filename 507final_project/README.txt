Project Overview
This project is a tool for analyzing and visualizing co-authorship networks in academic articles.
The user is prompted to enter a category of articles (Physics, Mathematics, Computer Science, Quantitative Biology, Quantitative Finance, or Statistics), and the program then loads a random sample of 50 articles from the corresponding category.
The co-authorship network is visualized using a graph, where nodes represent authors and edges represent co-authorship relationships.
There are also comparison visualizations that allow a user to input a specific author and then they can see their specific network and if they are the most influential author.
If they are not the most influential, they will be compared to the author with the most unique co-authors.

User Interactions
The user is prompted to enter the category of articles they would like to search for.
The valid categories are Physics, Mathematics, Computer Science, Quantitative Biology, Quantitative Finance, and Statistics.
If the user enters an invalid category, they are asked to try again.
The user is also asked to input an author name where they will then see that specific author's network.

Dependencies
This project requires the following Python packages:

networkx
matplotlib
arxiv
json
random

Network Organization
The co-authorship network is represented as a graph, where:
Nodes represent authors.
Edges represent co-authorship relationships.
An edge exists between two nodes if the corresponding authors have co-authored at least one article.
This edge has more weight if two authors have many published papers together.
