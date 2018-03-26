from newsapi.articles import Articles


if __name__ == "__main__":
    a = Articles(API_KEY="b606d265657f48699bf069618a0f749e")

    p = a.get(source="cnn")

    articles = p['articles']

    with open('news_sentences.txt', 'a') as f:
        for a in articles:
            f.write(a['title'] + "\n")
            f.write(a['description'] + "\n")



