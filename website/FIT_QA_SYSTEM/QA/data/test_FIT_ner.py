import spacy

sentences = ["Who is the instructor of Artificial Intelligence?",
             "Where is the classroom of Compiler Theory and Design?",
             "Where is Frederick C. Crawford Bldg?",
             "Where is 420CRF?",
             "Where is Panther Dining Hall?",
             "When is CSE5232?"]

def test_ner(output_dir, test_text):
    print("Loading from", output_dir)
    nlp2 = spacy.load(output_dir)
    doc2 = nlp2(test_text)
    for ent in doc2.ents:
        print(ent.label_, ent.text)

if __name__ == "__main__":
    for s in sentences:
        test_ner("FIT_model", s)