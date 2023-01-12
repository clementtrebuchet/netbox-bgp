import django_tables2 as tables
from django.utils.safestring import mark_safe

from netbox.tables import NetBoxTable
from netbox.tables.columns import ChoiceFieldColumn, TagColumn
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

AVAILABLE_LABEL = mark_safe('<span class="label label-success">Available</span>')
COL_TENANT = """
 {% if record.tenant %}
     <a href="{{ record.tenant.get_absolute_url }}" title="{{ record.tenant.description }}">{{ record.tenant }}</a>
 {% else %}
     &mdash;
 {% endif %}
 """

POLICIES = """
{% for rp in value.all %}
    <a href="{{ rp.get_absolute_url }}">{{ rp }}</a>{% if not forloop.last %}<br />{% endif %}
{% empty %}
    &mdash;
{% endfor %}
"""

COL_PASSWORD = """
{% if record.password %}
<a href="{{ record.get_absolute_url }}">
<input type='password' id='password{{ record.id }}' value="{{ record.password }}" disabled style="color: #0d6efd"></a>
<i class="mdi mdi-eye text-success" id="togglePassword{{ record.id }}" onclick="showPassword{{ record.id }}()" style="cursor: pointer; margin-left: -30px; z-index: 100;"></i>
<script>
    function showPassword{{ record.id }}() {
        var input_type = document.getElementById("password{{ record.id }}");
        var toggle_class = document.getElementById("togglePassword{{ record.id }}")
        if (input_type.type === "password") {
            input_type.type = "text";
            toggle_class.classList.remove("mdi", "mdi-eye")
            toggle_class.classList.add("mdi", "mdi-eye-off")
        } else {
            input_type.type = "password";
            toggle_class.classList.remove("mdi", "mdi-eye-off")
            toggle_class.classList.add("mdi", "mdi-eye")
        }
    }
</script>
{% else %}
     &mdash;
{% endif %}    
"""


class CommunityTable(NetBoxTable):
    value = tables.LinkColumn()
    status = ChoiceFieldColumn(default=AVAILABLE_LABEL)
    tenant = tables.TemplateColumn(template_code=COL_TENANT)
    tags = TagColumn(url_name="plugins:netbox_bgp:community_list")

    class Meta(NetBoxTable.Meta):
        model = Community
        fields = ("pk", "value", "description", "status", "tenant", "tags")
        default_columns = ("pk", "value", "description", "status", "tenant")


class BGPSessionTable(NetBoxTable):
    name = tables.LinkColumn()
    device = tables.LinkColumn()
    vrf = tables.LinkColumn()
    local_address = tables.LinkColumn()
    local_as = tables.LinkColumn()
    remote_address = tables.LinkColumn()
    remote_as = tables.LinkColumn()
    site = tables.LinkColumn()
    peer_group = tables.LinkColumn()
    status = ChoiceFieldColumn(default=AVAILABLE_LABEL)
    tenant = tables.TemplateColumn(template_code=COL_TENANT)
    password = tables.TemplateColumn(template_code=COL_PASSWORD)

    class Meta(NetBoxTable.Meta):
        model = BGPSession
        fields = (
            "pk",
            "name",
            "device",
            "vrf" "local_address",
            "local_as",
            "remote_address",
            "remote_as",
            "description",
            "peer_group",
            "site",
            "status",
            "tenant",
            "password",
        )
        default_columns = (
            "pk",
            "name",
            "device",
            "vrf",
            "local_address",
            "local_as",
            "remote_address",
            "remote_as",
            "description",
            "site",
            "status",
            "tenant",
            "password",
        )


class RoutingPolicyTable(NetBoxTable):
    name = tables.LinkColumn()

    class Meta(NetBoxTable.Meta):
        model = RoutingPolicy
        fields = ("pk", "name", "description")


class BGPPeerGroupTable(NetBoxTable):
    name = tables.LinkColumn()
    import_policies = tables.TemplateColumn(template_code=POLICIES, orderable=False)
    export_policies = tables.TemplateColumn(template_code=POLICIES, orderable=False)
    tags = TagColumn(url_name="plugins:netbox_bgp:peer_group_list")
    password = tables.TemplateColumn(template_code=COL_PASSWORD)

    class Meta(NetBoxTable.Meta):
        model = BGPPeerGroup
        fields = (
            "pk",
            "name",
            "description",
            "tags",
            "import_policies",
            "export_policies",
            "password",
        )
        default_columns = ("pk", "name", "description", "password")


class RoutingPolicyRuleTable(NetBoxTable):
    routing_policy = tables.Column(linkify=True)
    index = tables.Column(linkify=True)
    action = ChoiceFieldColumn()

    class Meta(NetBoxTable.Meta):
        model = RoutingPolicyRule
        fields = (
            "pk",
            "routing_policy",
            "index",
            "match_statements",
            "set_statements",
            "action",
            "description",
        )


class PrefixListTable(NetBoxTable):
    name = tables.LinkColumn()

    class Meta(NetBoxTable.Meta):
        model = PrefixList
        fields = ("pk", "name", "description")


class PrefixListRuleTable(NetBoxTable):
    prefix_list = tables.Column(linkify=True)
    index = tables.Column(linkify=True)
    action = ChoiceFieldColumn()
    network = tables.Column(
        verbose_name="Prefix",
        linkify=True,
    )

    class Meta(NetBoxTable.Meta):
        model = PrefixListRule
        fields = ("pk", "prefix_list", "index", "action", "network", "ge", "le")


class PasswordTable(NetBoxTable):
    password = tables.TemplateColumn(template_code=COL_PASSWORD)

    class Meta(NetBoxTable.Meta):
        model = Password
        fields = (
            "pk",
            "password",
        )
