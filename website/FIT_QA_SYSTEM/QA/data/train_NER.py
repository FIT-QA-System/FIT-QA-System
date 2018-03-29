from __future__ import unicode_literals, print_function
import spacy
import random
from spacy.gold import GoldParse
from spacy.language import EntityRecognizer
import pickle



import plac
from pathlib import Path


# LABEL = ['FIT_BUILDING', "FIT_COURSE"]
TRAIN_DATA = pickle.load(open("./training_sentences.txt", "rb"))
nlp = spacy.load('en_core_web_sm', entity=False, parser=False)
print(len(TRAIN_DATA))


# training data
# Note: If you're using an existing model, make sure to mix in examples of
# other entity types that spaCy correctly recognized before. Otherwise, your
# model might learn the new type, but "forget" what it previously knew.
# https://explosion.ai/blog/pseudo-rehearsal-catastrophic-forgetting
# TRAIN_DATA = [
#     ("Horses are too tall and they pretend to care about your feelings", {
#         'entities': [(0, 6, 'ANIMAL')]
#     }),
#
#     ("Do they bite?", {
#         'entities': []
#     }),
#
#     ("horses are too tall and they pretend to care about your feelings", {
#         'entities': [(0, 6, 'ANIMAL')]
#     }),
#
#     ("horses pretend to care about your feelings", {
#         'entities': [(0, 6, 'ANIMAL')]
#     }),
#
#     ("they pretend to care about your feelings, those horses", {
#         'entities': [(48, 54, 'ANIMAL')]
#     }),
#
#     ("horses?", {
#         'entities': [(0, 6, 'ANIMAL')]
#     })
# ]


@plac.annotations(
    model=("Model name. Defaults to blank 'en' model.", "option", "m", str),
    new_model_name=("New model name for model meta.", "option", "nm", str),
    output_dir=("Optional output directory", "option", "o", Path),
    n_iter=("Number of training iterations", "option", "n", int))
def main(model='en_core_web_sm', new_model_name='FIT', output_dir="FIT_model", n_iter=1):
    """Set up the pipeline and entity recognizer, and train the new entity."""
    if model is not None:
        nlp = spacy.load(model)  # load existing spaCy model
        print("Loaded model '%s'" % model)
    else:
        nlp = spacy.blank('en')  # create blank Language class
        print("Created blank 'en' model")

    # Add entity recognizer to model if it's not in the pipeline
    # nlp.create_pipe works for built-ins that are registered with spaCy
    if 'ner' not in nlp.pipe_names:
        ner = nlp.create_pipe('ner')
        nlp.add_pipe(ner)
    # otherwise, get it, so we can add labels to it
    else:
        ner = nlp.get_pipe('ner')

    # ner.add_label(LABEL)   # add new entity label to entity recognizer
    # ner.add_label("ANIMAL")
    ner.add_label("FIT_COURSE")
    ner.add_label("FIT_BUILDING")

    # get names of other pipes to disable them during training
    other_pipes = [pipe for pipe in nlp.pipe_names if pipe != 'ner']
    with nlp.disable_pipes(*other_pipes):  # only train NER
        optimizer = nlp.begin_training()
        for itn in range(n_iter):
            random.shuffle(TRAIN_DATA)
            losses = {}
            for text, annotations in TRAIN_DATA:
                print(text)
                nlp.update([text], [annotations], sgd=optimizer, drop=0.35,
                           losses=losses)
            print(losses)

    # test the trained model
    test_text = 'Where is the classroom of Artificial Intelligence?'
    doc = nlp(test_text)
    print("Entities in '%s'" % test_text)
    for ent in doc.ents:
        print(ent.label_, ent.text)

    # save model to output directory
    if output_dir is not None:
        output_dir = Path(output_dir)
        if not output_dir.exists():
            output_dir.mkdir()
        nlp.meta['name'] = new_model_name  # rename model
        nlp.to_disk(output_dir)
        print("Saved model to", output_dir)

        # test the saved model
        print("Loading from", output_dir)
        nlp2 = spacy.load(output_dir)
        doc2 = nlp2(test_text)
        for ent in doc2.ents:
            print(ent.label_, ent.text)


if __name__ == "__main__":
    # train()
    plac.call(main)

