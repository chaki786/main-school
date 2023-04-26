from django import template
from polls.models import Notification

register = template.Library()

@register.inclusion_tag('notificationt/show_notification.html', takes_context=True)
def show_notifications(context):
	request_user = context['request'].user
	notifications = Notification.objects.filter(to_user=request_user).exclude(user_has_seen=True).order_by('-date')
	for notification in notifications:
		if notification.notification_type == 'post':
			image_url = notification.post.image_url 
		elif notification.notification_type == 'follow':
			image_url = notification.followed_user.profile_picture_url 
		else:
			image_url = None
			notification.image_url = image_url
	return {'notifications': notifications}