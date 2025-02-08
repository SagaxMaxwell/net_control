import wmi
from wmi import WMI
from wmi import _wmi_object
from typing import List


class AdapterCenter:
    wmi_client = wmi.WMI()

    @staticmethod
    def get_adapters() -> List[_wmi_object]:
        adpaters = list()
        adpaters.extend(AdapterCenter.wmi_client.Win32_NetworkAdapterConfiguration())
        return adpaters

    @staticmethod
    def get_adpater_by_description(description: str) -> _wmi_object:
        for adapter in AdapterCenter.get_adapters():
            if adapter.Description == description:
                return adapter
        return None

    @staticmethod
    def get_adpater_by_ipv4(ipv4: str) -> _wmi_object:
        for adapter in AdapterCenter.get_adapters():
            current_ipv4, current_ipv6 = adapter.IPAddress
            if current_ipv4 == ipv4:
                return adapter
        return None

    @staticmethod
    def set_ipv4(adapter: _wmi_object, ipv4: str, subnet_mask: str) -> bool:
        result = adapter.EnableStatic(IPAddress=[ipv4], SubnetMask=[subnet_mask])
        return set(result) <= {0, 1}

    @staticmethod
    def set_dhcp(adapter: _wmi_object) -> bool:
        result = adapter.EnableDHCP()
        return set(result) <= {0, 1}

    def set_vlan_id(self, adapter: _wmi_object, vlan_id: int) -> bool:
        net_adapters = self.wmi_client.Win32_NetworkAdapter(
            Description=adapter.Description
        )
        interface_index = net_adapters.pop().InterfaceIndex
        adapters = WMI(namespace="root/StandardCimv2").MSFT_NetAdapterVlan(
            InterfaceIndex=interface_index
        )
        adapter_msft = adapters.pop()
        result = adapter_msft.SetVlanID(VlanID=vlan_id)
        return set(result) in {0}

    def set_speed_duplex(self, adapter: _wmi_object, speed_duplex: int) -> bool:
        net_adapters = self.wmi_client.Win32_NetworkAdapter(
            Description=adapter.Description
        )
        interface_index = net_adapters.pop().InterfaceIndex
        adapters = WMI(namespace="root/StandardCimv2").MSFT_NetAdapter(
            InterfaceIndex=interface_index
        )
        adapter_msft = adapters.pop()
        adapter_msft.SpeedDuplex = speed_duplex
        adapter_msft.put()
        return True
