import pickle, pprint
import scrapy


class QA:
    def __init__(self, q, a, url, category):
        self.question = q
        self.answer = a
        self.url = url
        self.category = category


def pickle_data(data, filename):
    output_file = open(filename + '.pkl', 'wb')
    pickle.dump(data, output_file)
    output_file.close()


def unpickle_data(filename):
    input_file = open(filename + '.pkl', 'rb')
    data = pickle.load(input_file)
    pprint.pprint(input_file)
    input_file.close()
    return data


if __name__ == "__main__":
    # first = QA("This is the question", "This is the answer", "www.google.com", "category1")
    # output = open('data.pkl', 'wb')
    # pickle.dump(first, output)

    input = open('data.pkl', 'rb')
    first = pickle.load(input)
    pprint.pprint(input)

    print(first.question)
