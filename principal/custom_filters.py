from django import template

register = template.Library()

@register.filter
def groupby_sender(messages):
    senders = {}
    for message in messages:
        sender = message.sender.username
        if sender not in senders:
            senders[sender] = []
        senders[sender].append(message)
    return senders
