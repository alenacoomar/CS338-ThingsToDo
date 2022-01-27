import spacy

nlp = spacy.load("en_core_web_sm")


# transcript = "I will set the table with the blue napkins. She is cool. Abby should go to the store and buy a cake.
# We can eat lunch at noon and I will get pizza. I like breakfast. Someone should paint the wall. Alena will do that.
# We need to clean the living room."

def analyse(transcript):
    sentences = transcript.split('.')
    all_sentences = [i for i in sentences if i]  # removes empty strings

    # 2. Go through each sentence and check for task patterns
    #    Save these sentences into new array as task_sentences
    task_sentences = []
    for s in all_sentences:
        processed = nlp(s)
        is_task = 0
        i = 0

        for token in processed:
            # if proper-noun/pronoun + 'will/should'
            if (token.pos_ == 'PROPN' or token.pos_ == 'PRON') and (token.text != 'It'):
                if (i + 1 < len(s.split())):
                    next_word = processed[i + 1].text
                    if (next_word == 'will') or (next_word == 'should'):
                        is_task = 1

            # if 'need to' in sentence
            if (is_task == 0) and (token.text == 'need'):
                if (i + 1 < len(s.split())):
                    next_word = processed[i + 1].text
                    if (next_word == 'to'):
                        is_task = 1

            i = i + 1

        if is_task == 1:
            task_sentences.append(s)

    return task_sentences
