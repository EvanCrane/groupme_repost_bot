# mention.py
from models import Mention
from models import Action
from response import mention_response

def handle_mention(request_params, mention):
    mention = Mention(mention['action_text'], mention['message_id'], mention['mentioned_by'], mention['full_message'])
    actions = get_actions()
    if actions != None:
        action = perform_action(actions, mention)
    response = mention_response(request_params, action.action_result, mention.message_id)
    return (mention, action, response)


def get_actions():
    actions = {
        'SHOW': ['COUNT']
    }
    return actions
    

def perform_action(actions, mention):
    if mention.message != '':
        primary_action = mention.message.split(' ')[0]
        if primary_action in actions:
            if len(mention.message.split(' ')) > 1:
                secondary_action = mention.message.split(' ')[1]
                if secondary_action in actions[primary_action]:
                    #perform both actions
                    action_data = "TEST DOUBLE ACTION"
                    action = Action(mention.message, action_data, mention)
                    return action
            #no secondary action specified return possible options
            usage = "usage: " + primary_action + " " + str(actions.get(primary_action))
            action = Action(mention.message, usage, mention)
            return action
    else:
        action = Action(mention.message, None, mention)
        return action


def log_action(mention, action_data):
    return True