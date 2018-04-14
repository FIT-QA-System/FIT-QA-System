import spacy

sentences = ["Who is the instructor of Artificial Intelligence?",
             "Where is the classroom of Compiler Theory and Design?",
             "Where is Frederick C. Crawford Bldg?",
             "Where is 420CRF?",
             "Where is Panther Dining Hall?",
             "When is CSE 5232?",
             "What is the capacity of 19839?",
             "Where is panther dining hall?"]


def test_ner(output_dir, test_texts):
    print("Loading from", output_dir)
    nlp2 = spacy.load(output_dir)
    for s in test_texts:
        doc2 = nlp2(s)
        for ent in doc2.ents:
            print(ent.label_, ent.text)

if __name__ == "__main__":
    test_ner("FIT_model_b_c_e", sentences)