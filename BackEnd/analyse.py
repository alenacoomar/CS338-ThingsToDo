# transcript = "I will set the table with the blue napkins. She is cool. Abby should go to the store and buy a cake.
# We can eat lunch at noon and I will get pizza. I like breakfast. Someone should paint the wall. Alena will do that.
# We need to clean the living room."

def analyse(transcript):
    import spacy
    nlp = spacy.load("en_core_web_sm")

    # Make into list of lists [name, words]
    import webvtt
    from io import StringIO

    name_transcript = []
    buffer = StringIO(transcript)
    for caption in webvtt.read_buffer(buffer):
        if ":" in caption.text:
            name_transcript.append(caption.text.split(":"))
        else:
            name_transcript.append(["Team", caption.text])  # if speaker unknown then assign as team

    all_tasks = []
    all_assignees = []
    curr_speaker = ""
    prev_speaker = ""

    # goes through each chunk of someone speaking
    for t in name_transcript:
        prev_speaker = curr_speaker
        curr_speaker = t[0]
        curr_tasks, curr_assigned_to = task_finder(nlp, t[1])

        if curr_tasks:
            all_tasks.append(curr_tasks)
            for a in curr_assigned_to:
                if a:  # not empty
                    if a == 'I':  # "I" --> current speaker
                        all_assignees.append(curr_speaker)
                    elif a == 'you':  # "You" --> previous speaker
                        all_assignees.append(prev_speaker)
                    else:
                        all_assignees.append(a)

    # Task Reassignment
    # "That" --> previous task and current speaker
    i = 0
    tasks_to_delete = []
    assignees_to_delete = []
    for task in all_tasks:
        if ('will do that' in task) or ('can do that' in task) or ('will do it' in task) or ('can do it' in task):
            all_tasks[i - 1] = all_tasks[i - 1].replace(all_assignees[i - 1], all_assignees[i])
            tasks_to_delete.append(i)
            assignees_to_delete.append(i - 1)
        i += 1

    # take out indicies that have reassignment
    final_tasks = []
    final_assignees = []
    for i in range(len(all_tasks)):
        if i not in tasks_to_delete:
            final_tasks.append(all_tasks[i])

    for i in range(len(all_assignees)):
        if i not in assignees_to_delete:
            final_assignees.append(all_assignees[i])

    return final_tasks, final_assignees


def task_finder(nlp, transcript):
    # Split transcript into sentences
    sentences = transcript.split('.')
    all_sentences = [i for i in sentences if i] # removes empty strings

    # Go through each sentence and check for task patterns
    # Save these sentences into new array as task_sentences
    task_sentences = []
    task_assigned_to = []
    for s in all_sentences:
        processed = nlp(s)
        is_task = 0
        i = 0
        assigned_to = "Team" # Default to entire team assigned to task

        for token in processed:
            # if proper-noun/pronoun + 'will/should'
            if (token.pos_ == 'PROPN' or token.pos_ == 'PRON') and (token.text != 'It'):
                if(i+1 < len(s.split())):
                    next_word = processed[i+1].text
                    if (next_word == 'will') or (next_word == 'should'):
                        is_task = 1
                        if (token.pos == 'PROPN') or (token.text == 'I') or (token.text == 'you'):
                            assigned_to = token.text

            # if '(need, needs) to' in sentence
            if (is_task == 0) and ((token.text == 'need') or (token.text == 'needs')):
                if(i+1 < len(s.split())):
                    next_word = processed[i+1].text
                    if (next_word == 'to'):
                        is_task = 1
                        if processed[i-1].pos_ == 'PROPN':
                            assigned_to = processed[i-1].text
                        elif (processed[i-1].text == 'I') or (processed[i-1].text == 'you'):
                            assigned_to = processed[i-1].text

            i = i + 1

        if is_task == 1:
            task_sentences.append(s)
            task_assigned_to.append(assigned_to)
    return task_sentences, task_assigned_to