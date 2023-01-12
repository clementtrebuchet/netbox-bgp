from rest_framework import routers

from .views import (
    BGPSessionViewSet,
    RoutingPolicyViewSet,
    BGPPeerGroupViewSet,
    CommunityViewSet,
    PrefixListViewSet,
    PasswordViewSet,
)

router = routers.DefaultRouter()
router.register("session", BGPSessionViewSet, "session")
router.register("bgpsession", BGPSessionViewSet, "bgpsession")
router.register("routing-policy", RoutingPolicyViewSet)
router.register("peer-group", BGPPeerGroupViewSet, "peergroup")
router.register("bgppeergroup", BGPPeerGroupViewSet, "bgppeergroup")
router.register("community", CommunityViewSet)
router.register("prefix-list", PrefixListViewSet)
router.register("password", PasswordViewSet)

urlpatterns = router.urls
