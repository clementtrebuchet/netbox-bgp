from rest_framework.viewsets import ModelViewSet

from netbox_bgp.filters import (
    BGPSessionFilterSet,
    RoutingPolicyFilterSet,
    BGPPeerGroupFilterSet,
    CommunityFilterSet,
    PrefixListFilterSet,
)
from netbox_bgp.models import (
    BGPSession,
    RoutingPolicy,
    BGPPeerGroup,
    Community,
    PrefixList,
    Password,
)
from .serializers import (
    BGPSessionSerializer,
    RoutingPolicySerializer,
    BGPPeerGroupSerializer,
    CommunitySerializer,
    PrefixListSerializer,
    PasswordSerializer,
)


class BGPSessionViewSet(ModelViewSet):
    queryset = BGPSession.objects.all()
    serializer_class = BGPSessionSerializer
    filterset_class = BGPSessionFilterSet


class RoutingPolicyViewSet(ModelViewSet):
    queryset = RoutingPolicy.objects.all()
    serializer_class = RoutingPolicySerializer
    filterset_class = RoutingPolicyFilterSet


class BGPPeerGroupViewSet(ModelViewSet):
    queryset = BGPPeerGroup.objects.all()
    serializer_class = BGPPeerGroupSerializer
    filterset_class = BGPPeerGroupFilterSet


class CommunityViewSet(ModelViewSet):
    queryset = Community.objects.all()
    serializer_class = CommunitySerializer
    filterset_class = CommunityFilterSet


class PrefixListViewSet(ModelViewSet):
    queryset = PrefixList.objects.all()
    serializer_class = PrefixListSerializer
    filterset_class = PrefixListFilterSet


class PasswordViewSet(ModelViewSet):
    queryset = Password.objects.all()
    serializer_class = PasswordSerializer
