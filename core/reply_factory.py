
from .constants import BOT_WELCOME_MESSAGE, PYTHON_QUESTION_LIST


def generate_bot_responses(message, session):
    bot_responses = []

    current_question_id = session.get("current_question_id")
    if not current_question_id:
        bot_responses.append(BOT_WELCOME_MESSAGE)

    success, error = record_current_answer(message, current_question_id, session)

    if not success:
        return [error]

    next_question, next_question_id = get_next_question(current_question_id)

    if next_question:
        bot_responses.append(next_question)
    else:
        final_response = generate_final_response(session)
        bot_responses.append(final_response)

    session["current_question_id"] = next_question_id
    session.save()

    return bot_responses


def record_current_answer(answer, current_question_id, session):
   '''
    Validates and stores the answer for the current question to the Django session.
    '''
    # Get the current question from the PYTHON_QUESTION_LIST based on the question ID
   current_question = PYTHON_QUESTION_LIST[current_question_id]

    # Validate if the provided answer is correct
   correct_answer = current_question['answer']
   if answer == correct_answer:
        # Store the answer in the session if it's correct
        session['answers'][current_question_id] = answer
        return True, ""  # Return success and an empty error message
   else:
        return False, "Incorrect answer"  # Return failure and an error message


def get_next_question(current_question_id):
    '''
    Fetches the next question from the PYTHON_QUESTION_LIST based on the current_question_id.
    '''
    next_question_id = current_question_id + 1
    if next_question_id < len(PYTHON_QUESTION_LIST):
        next_question = PYTHON_QUESTION_LIST[next_question_id]['question_text']
        return next_question, next_question_id
    else:
        return None, None  # Return None if there are no more questions




def generate_final_response(session):
    '''
    Creates a final result message including a score based on the answers
    by the user for questions in the PYTHON_QUESTION_LIST.
    '''

    num_correct_answers = 0
    total_questions = len(PYTHON_QUESTION_LIST)

    # Calculate the number of correct answers
    for question_id, question in enumerate(PYTHON_QUESTION_LIST):
        if question_id in session['answers'] and session['answers'][question_id] == question['answer']:
            num_correct_answers += 1

    # Calculate the score
    score = (num_correct_answers / total_questions) * 100

    # Generate the final response message
    final_response = f"You have completed the quiz.\n\n" \
                     f"Total questions: {total_questions}\n" \
                     f"Correct answers: {num_correct_answers}\n" \
                     f"Score: {score:.2f}%"
    
    return final_response
