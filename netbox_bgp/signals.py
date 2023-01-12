from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import BGPSession


@receiver(post_save, sender=BGPSession)
def assign_password(sender, instance, **kwargs):
    """
    Assign a new password to a BGPSession inheriting from a BGPPeerGroup

    :param instance: instance of BGPSession
    :param kwargs: extra parameters
    :param sender: the signal sender
    """
    session = BGPSession.objects.get(id=instance.id)
    if not session.password and session.peer_group:
        if session.peer_group.password:
            session.password = session.peer_group.password
            session.full_clean()
            post_save.disconnect(assign_password, sender=BGPSession)
            session.save()
            post_save.connect(assign_password, sender=BGPSession)
