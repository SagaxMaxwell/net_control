from modules import *


if __name__ == "__main__":
    adapter_configuration = AdapterConfiguration()
    adapter_configuration.load_configurations()
    for adapter in AdapterCenter.get_adapters():
        if adapter.Description == "Intel(R) Wi-Fi 6 AX201 160MHz":
            print(adapter.Description)
