from django import forms
from django.core.exceptions import (
    MultipleObjectsReturned,
    ObjectDoesNotExist,
)
from django.utils.translation import gettext as _

from dcim.models import Device, Site
from extras.models import Tag
from ipam.formfields import IPNetworkFormField
from ipam.models import IPAddress, Prefix, ASN, VRF
from netbox.forms import (
    NetBoxModelForm,
    NetBoxModelBulkEditForm,
    NetBoxModelFilterSetForm,
)
from tenancy.models import Tenant
from utilities.forms import (
    DynamicModelChoiceField,
    DynamicModelMultipleChoiceField,
    StaticSelect,
    APISelect,
    APISelectMultiple,
    StaticSelectMultiple,
    TagFilterField,
)
from .choices import SessionStatusChoices, CommunityStatusChoices
from .models import (
    Community,
    BGPSession,
    RoutingPolicy,
    BGPPeerGroup,
    RoutingPolicyRule,
    PrefixList,
    PrefixListRule,
    Password,
)


class CommunityForm(NetBoxModelForm):
    tags = DynamicModelMultipleChoiceField(queryset=Tag.objects.all(), required=False)
    status = forms.ChoiceField(
        required=False, choices=CommunityStatusChoices, widget=StaticSelect()
    )
    tenant = DynamicModelChoiceField(queryset=Tenant.objects.all(), required=False)

    class Meta:
        model = Community
        fields = [
            "value",
            "description",
            "status",
            "tenant",
            "tags",
        ]


class CommunityFilterForm(NetBoxModelFilterSetForm):
    q = forms.CharField(required=False, label="Search")
    tenant = DynamicModelChoiceField(queryset=Tenant.objects.all(), required=False)
    status = forms.MultipleChoiceField(
        choices=CommunityStatusChoices, required=False, widget=StaticSelectMultiple()
    )
    site = DynamicModelChoiceField(queryset=Site.objects.all(), required=False)

    tag = TagFilterField(Community)

    model = Community


class CommunityBulkEditForm(NetBoxModelBulkEditForm):
    pk = forms.ModelMultipleChoiceField(
        queryset=Community.objects.all(), widget=forms.MultipleHiddenInput
    )
    tenant = DynamicModelChoiceField(queryset=Tenant.objects.all(), required=False)
    description = forms.CharField(max_length=200, required=False)
    status = forms.ChoiceField(
        required=False, choices=CommunityStatusChoices, widget=StaticSelect()
    )

    model = Community
    nullable_fields = [
        "tenant",
        "description",
    ]


class BGPSessionForm(NetBoxModelForm):
    name = forms.CharField(max_length=64, required=True)
    tags = DynamicModelMultipleChoiceField(queryset=Tag.objects.all(), required=False)
    site = DynamicModelChoiceField(queryset=Site.objects.all(), required=False)
    device = DynamicModelChoiceField(
        queryset=Device.objects.all(), required=False, query_params={"site_id": "$site"}
    )
    vrf = DynamicModelChoiceField(queryset=VRF.objects.all(), required=False)
    tenant = DynamicModelChoiceField(queryset=Tenant.objects.all(), required=False)
    local_as = DynamicModelChoiceField(
        queryset=ASN.objects.all(),
        query_params={"site_id": "$site"},
        label=_("Local AS"),
    )
    remote_as = DynamicModelChoiceField(
        queryset=ASN.objects.all(), label=_("Remote AS")
    )
    local_address = DynamicModelChoiceField(
        queryset=IPAddress.objects.all(), query_params={"device_id": "$device"}
    )
    remote_address = DynamicModelChoiceField(
        queryset=IPAddress.objects.all(),
    )
    peer_group = DynamicModelChoiceField(
        queryset=BGPPeerGroup.objects.all(),
        required=False,
        widget=APISelect(
            api_url="/api/plugins/bgp/peer-group/",
        ),
    )
    import_policies = DynamicModelMultipleChoiceField(
        queryset=RoutingPolicy.objects.all(),
        required=False,
        widget=APISelectMultiple(api_url="/api/plugins/bgp/routing-policy/"),
    )
    export_policies = DynamicModelMultipleChoiceField(
        queryset=RoutingPolicy.objects.all(),
        required=False,
        widget=APISelectMultiple(api_url="/api/plugins/bgp/routing-policy/"),
    )

    password = DynamicModelChoiceField(queryset=Password.objects.all(), required=False)

    class Meta:
        model = BGPSession
        fields = [
            "name",
            "site",
            "device",
            "vrf",
            "local_as",
            "remote_as",
            "local_address",
            "remote_address",
            "description",
            "status",
            "peer_group",
            "tenant",
            "tags",
            "password",
            "import_policies",
            "export_policies",
        ]
        fieldsets = (
            (
                "Session",
                (
                    "name",
                    "site",
                    "device",
                    "vrf" "description",
                    "status",
                    "peer_group",
                    "tenant",
                    "tags",
                    "password",
                ),
            ),
            ("Remote", ("remote_as", "remote_address")),
            ("Local", ("local_as", "local_address")),
            ("Policies", ("import_policies", "export_policies")),
        )
        widgets = {
            "status": StaticSelect(),
        }


class BGPSessionAddForm(BGPSessionForm):
    remote_address = IPNetworkFormField()

    def clean_remote_address(self):
        try:
            ip = IPAddress.objects.get(address=str(self.cleaned_data["remote_address"]))
        except MultipleObjectsReturned:
            ip = IPAddress.objects.filter(
                address=str(self.cleaned_data["remote_address"])
            ).first()
        except ObjectDoesNotExist:
            ip = IPAddress.objects.create(
                address=str(self.cleaned_data["remote_address"])
            )
        self.cleaned_data["remote_address"] = ip
        return self.cleaned_data["remote_address"]


class BGPSessionFilterForm(NetBoxModelFilterSetForm):
    model = BGPSession
    q = forms.CharField(required=False, label="Search")
    remote_as_id = DynamicModelMultipleChoiceField(
        queryset=ASN.objects.all(), required=False, label=_("Remote AS")
    )
    local_as_id = DynamicModelMultipleChoiceField(
        queryset=ASN.objects.all(), required=False, label=_("Local AS")
    )
    by_local_address = forms.CharField(required=False, label="Local Address")
    by_remote_address = forms.CharField(required=False, label="Remote Address")
    device_id = DynamicModelMultipleChoiceField(
        queryset=Device.objects.all(), required=False, label=_("Device")
    )
    status = forms.MultipleChoiceField(
        choices=SessionStatusChoices, required=False, widget=StaticSelectMultiple()
    )
    peer_group = DynamicModelMultipleChoiceField(
        queryset=BGPPeerGroup.objects.all(),
        required=False,
        widget=APISelectMultiple(api_url="/api/plugins/bgp/peer-group/"),
    )
    import_policies = DynamicModelMultipleChoiceField(
        queryset=RoutingPolicy.objects.all(),
        required=False,
        widget=APISelectMultiple(api_url="/api/plugins/bgp/routing-policy/"),
    )
    export_policies = DynamicModelMultipleChoiceField(
        queryset=RoutingPolicy.objects.all(),
        required=False,
        widget=APISelectMultiple(api_url="/api/plugins/bgp/routing-policy/"),
    )
    tenant = DynamicModelChoiceField(queryset=Tenant.objects.all(), required=False)

    tag = TagFilterField(model)


class RoutingPolicyFilterForm(NetBoxModelFilterSetForm):
    model = RoutingPolicy
    q = forms.CharField(required=False, label="Search")

    tag = TagFilterField(model)


class RoutingPolicyForm(NetBoxModelForm):
    tags = DynamicModelMultipleChoiceField(queryset=Tag.objects.all(), required=False)

    class Meta:
        model = RoutingPolicy
        fields = ["name", "description", "tags"]


class BGPPeerGroupFilterForm(NetBoxModelFilterSetForm):
    model = BGPPeerGroup
    q = forms.CharField(required=False, label="Search")

    tag = TagFilterField(model)


class BGPPeerGroupForm(NetBoxModelForm):
    import_policies = DynamicModelMultipleChoiceField(
        queryset=RoutingPolicy.objects.all(),
        required=False,
        widget=APISelectMultiple(api_url="/api/plugins/bgp/routing-policy/"),
    )
    export_policies = DynamicModelMultipleChoiceField(
        queryset=RoutingPolicy.objects.all(),
        required=False,
        widget=APISelectMultiple(api_url="/api/plugins/bgp/routing-policy/"),
    )
    tags = DynamicModelMultipleChoiceField(queryset=Tag.objects.all(), required=False)

    password = DynamicModelChoiceField(queryset=Password.objects.all(), required=False)

    class Meta:
        model = BGPPeerGroup
        fields = [
            "name",
            "description",
            "import_policies",
            "export_policies",
            "tags",
            "password",
        ]


class RoutingPolicyRuleForm(NetBoxModelForm):
    continue_entry = forms.IntegerField(
        required=False,
        label="Continue",
        help_text="Null for disable, 0 to next entry, or any sequence number",
    )
    match_community = DynamicModelMultipleChoiceField(
        queryset=Community.objects.all(),
        required=False,
    )
    match_ip_address = DynamicModelMultipleChoiceField(
        queryset=PrefixList.objects.all(),
        required=False,
        label="Match IP address Prefix lists",
    )
    match_ipv6_address = DynamicModelMultipleChoiceField(
        queryset=PrefixList.objects.all(),
        required=False,
        label="Match IPv6 address Prefix lists",
    )
    match_custom = forms.JSONField(
        label="Custom Match",
        help_text='Any custom match statements, e.g., {"ip nexthop": "1.1.1.1"}',
        required=False,
    )
    set_actions = forms.JSONField(
        label="Set statements",
        help_text='Set statements, e.g., {"as-path prepend": [12345,12345]}',
        required=False,
    )

    class Meta:
        model = RoutingPolicyRule
        fields = [
            "routing_policy",
            "index",
            "action",
            "continue_entry",
            "match_community",
            "match_ip_address",
            "match_ipv6_address",
            "match_custom",
            "set_actions",
            "description",
        ]


class PrefixListFilterForm(NetBoxModelFilterSetForm):
    model = PrefixList
    q = forms.CharField(required=False, label="Search")

    tag = TagFilterField(model)


class PrefixListForm(NetBoxModelForm):
    tags = DynamicModelMultipleChoiceField(queryset=Tag.objects.all(), required=False)

    class Meta:
        model = PrefixList
        fields = ["name", "description", "tags"]


class PrefixListRuleForm(NetBoxModelForm):
    prefix = DynamicModelChoiceField(
        queryset=Prefix.objects.all(),
        required=False,
        help_text="NetBox Prefix Object",
    )
    prefix_custom = IPNetworkFormField(
        required=False,
        label="Prefix",
        help_text="Just IP field for define special prefix like 0.0.0.0/0",
    )
    ge = forms.IntegerField(
        label="Greater than or equal to",
        required=False,
    )
    le = forms.IntegerField(
        label="Less than or equal to",
        required=False,
    )

    class Meta:
        model = PrefixListRule
        fields = [
            "prefix_list",
            "index",
            "action",
            "prefix",
            "prefix_custom",
            "ge",
            "le",
        ]


class PasswordForm(NetBoxModelForm):
    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
    )
    confirm_password = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
    )

    class Meta:
        model = Password
        fields = ["password"]

    def clean(self):
        cleaned_data = super(PasswordForm, self).clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError("Passwords do not match")
