from graphviz import Graph
from natasha import (
    Segmenter,
    MorphVocab,

    NewsEmbedding,
    NewsMorphTagger,
    NewsSyntaxParser,
    NewsNERTagger,

    Doc
)

segmenter = Segmenter()
morph_vocab = MorphVocab()

emb = NewsEmbedding()
morph_tagger = NewsMorphTagger(emb)
syntax_parser = NewsSyntaxParser(emb)
ner_tagger = NewsNERTagger(emb)

dot = Graph(comment="Room")


def main():
    print("Enter each statement line by line.\n"
          "When you're finished entering statement press Enter again.\n")

    lines = []

    print("Enter text:", end=" ")
    new_line = input()

    while new_line != "":
        lines.append(new_line)
        new_line = input()

    lemmas_array = []
    action_word = "соединить"

    for line in lines:
        print()
        doc = Doc(line)
        doc.segment(segmenter)
        doc.tag_morph(morph_tagger)

        flag = False
        rooms = []
        tokens = doc.tokens

        for i in range(len(tokens)):
            tokens[i].lemmatize(morph_vocab)

            # If the word means `connect`
            if tokens[i].lemma == action_word:
                # Then set the flag to True
                flag = True
                # If the word has a negative meaning, then set the flag to False
                if i > 0 \
                        and tokens[i - 1].feats.get("Polarity") == "Neg":
                    flag = False

        # Checks if there is an action word in the statement
        if not flag:
            continue

        # Run through every word
        for i in range(len(tokens)):
            # If the word is Noun, Adjective or Proposition
            if tokens[i].pos == "NOUN" \
                    or tokens[i].pos == "PROPN" \
                    or tokens[i].pos == "ADJ":
                # If there is a numeric before the word
                # then the word proably means count of something
                if i > 0 and tokens[i - 1].pos == "NUM":
                    continue

                # Append the word to the listed rooms in the statement
                rooms.append(tokens[i])
                # Append the word to all found lemmas
                if tokens[i].lemma not in lemmas_array:
                    lemmas_array.append(tokens[i].lemma)

        # For every room found in statement
        # Connect each with each
        for room in rooms:
            for another_room in rooms:
                if room.lemma != another_room.lemma:
                    dot.edge(room.lemma, another_room.lemma)

    print(dot.source)
    dot.render("graph.gv")


if __name__ == '__main__':
    main()
