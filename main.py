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
    print("Enter each sentence line by line.\n"
          "When you're finished entering sentences press Enter again.\n")

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

            if tokens[i].lemma == action_word:
                flag = True
                if i > 0 \
                        and tokens[i - 1].feats.get("Polarity") == "Neg":
                    flag = False

        if not flag:
            continue

        for i in range(len(tokens)):
            if tokens[i].pos == "NOUN" \
                    or tokens[i].pos == "PROPN" \
                    or tokens[i].pos == "ADJ":
                if i > 0 and tokens[i - 1].pos == "NUM":
                    continue

                rooms.append(tokens[i])
                if tokens[i].lemma not in lemmas_array:
                    lemmas_array.append(tokens[i].lemma)

        for room in rooms:
            for another_room in rooms:
                if room.lemma != another_room.lemma:
                    print(room, another_room)
                    dot.edge(room.lemma, another_room.lemma)

    print(dot.source)
    dot.render("test.gv")


if __name__ == '__main__':
    main()
