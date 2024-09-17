from netbox.views import generic
from django.utils.translation import gettext as _
from django.template.defaulttags import register
from utilities.views import ViewTab, register_model_view
from ipam.models import Prefix
from ipam.choices import IPAddressStatusChoices,IPRangeStatusChoices
import netaddr

@register_model_view(Prefix, 'ipmap', path='ip-map')
class PrefixMapView(generic.ObjectView):
    queryset = Prefix.objects.all()
    template_name = 'netbox_prefix_map/prefix_map.html'
    tab = ViewTab(
        label=_('IP Map'),
        permission='ipam.view_ipaddress',
        weight=1000
    )

    # Used in the prefix_map.html template
    @register.filter
    def get_value(dictionary, key):
        return dictionary.get(key)

    def get_ip_list(self, request, instance):
        prefix = netaddr.IPNetwork(instance.prefix)
        child_ips = list(instance.get_child_ips().restrict(request.user, 'view'))
        child_ranges = list(instance.get_child_ranges().restrict(request.user, 'view'))
        choices = self.get_choices()

        ip_list = []
        status_count = {}
        for ip in prefix:
            #          ip       ip pk      range pk   status
            ip_info = [str(ip), None,      None,      'available']
            for child_range in child_ranges:
                # If the IP is inside the range
                if ip in child_range.range:
                    ip_info[2] = child_range.pk
                    ip_info[3] = child_range.status
            for child_ip in child_ips:
                # If the IP is the same as one of the child IP of the prefix
                if ip == child_ip.address.ip:
                    ip_info[1] = child_ip.pk
                    ip_info[3] = child_ip.status
            
            # If the IP is a special IP (first (non-useable) IP or last (non-useable) IP (broadcast))
            if ip == prefix.ip or ip == prefix.broadcast:
                ip_info[3] = 'reserved'
            
            # Count the number of time the statuses appear
            if ip_info[3] in status_count:
                status_count[ip_info[3]] += 1
            else:
                status_count[ip_info[3]] = 1

            # Add the correct status tuple (name, display name, color)
            for choice in choices:
                if choice[0] == ip_info[3]:
                    ip_info[3] = choice
                    break

            ip_list.append(tuple(ip_info))

        return (ip_list,status_count)
    
    # Merge both IP possibles statuses and range possibles statuses
    def get_choices(self):
        # Firstly add the 'available' status that cannot be added to an IP or a range
        choices = [('available', _('Available'), 'success')]
        for choice in IPAddressStatusChoices.CHOICES:
            choices.append(choice)
        for choice in IPRangeStatusChoices.CHOICES:
            if choice not in choices:
                choices.append(choice)
        return choices

    # Give those variables to the template
    def get_extra_context(self, request, instance):
        return {
            'first_available_ip': instance.get_first_available_ip(),
            'ip_list': self.get_ip_list(request, instance),
            'choices': self.get_choices(),
        }