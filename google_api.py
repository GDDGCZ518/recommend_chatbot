from scholarly import scholarly

# print(next(scholarly.search_author('Steven A. Cholewiak')))

# 检索作者的个人资料
# Retrieve the author's data, fill-in, and print
# search_query = scholarly.search_author('Hao Siyu')
# author = scholarly.fill(next(search_query))
# print(author)

# # Print the titles of the author's publications
# print([pub['bib']['title'] for pub in author['publications']])

# # Take a closer look at the first publication
# pub = scholarly.fill(author['publications'][0])
# print(pub)

# # Which papers cited that publication?
# print([citation['bib']['title'] for citation in scholarly.citedby(pub)])

search_query = scholarly.search_pubs('3D objects')
# scholarly.pprint(next(search_query))
print(search_query)
for x in search_query:
    print(x)

