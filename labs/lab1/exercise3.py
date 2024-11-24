import json
from datetime import datetime


class DeviceCatalog:
    def __init__(self, file_path):
        self.file_path = file_path
        self.load_catalog()

    def load_catalog(self):
        with open(self.file_path, 'r') as file:
            self.catalog_data = json.load(file)

    def save_catalog(self):
        with open(self.file_path, 'w') as file:
            json.dump(self.catalog_data, file, indent=4)

    def search_by_name(self, name):
        found_devices = []
        for device in self.catalog_data['devicesList']:
            if device['deviceName'] == name:
                found_devices.append(device)
        return found_devices

    def search_by_id(self, device_id):
        for device in self.catalog_data['devicesList']:
            if device['deviceID'] == device_id:
                return device
        return None

    def search_by_service(self, service):
        found_devices = []
        for device in self.catalog_data['devicesList']:
            if service in device['availableServices']:
                found_devices.append(device)
        return found_devices

    def search_by_measure_type(self, measure_type):
        found_devices = []
        for device in self.catalog_data['devicesList']:
            if measure_type in device['measureType']:
                found_devices.append(device)
        return found_devices

    def insert_device(self, new_device=None):
        """
        import os
            if new_device is None:
                # Read 'new_device.json' if no specific device is provided
                new_device_path = os.path.join(os.path.dirname(__file__), "new_device.json")
                try:
                    with open(new_device_path, 'r') as file:
                        new_device = json.load(file)
                except FileNotFoundError:
                    print(f"File '{new_device_path}' not found. Please ensure it is in the correct location.")
                    return
                except json.JSONDecodeError as e:
                    print("Invalid JSON format in 'new_device.json'. Please correct the file and try again.")
                    return
        """

        # Check if the device already exists in the catalog
        existing_device = self.search_by_id(new_device['deviceID'])
        if existing_device:
            print("Device already exists. Updating information.")
            existing_device.update(new_device)
            existing_device['lastUpdate'] = datetime.now().strftime("%Y-%m-%d %H:%M")
        else:
            new_device['lastUpdate'] = datetime.now().strftime("%Y-%m-%d %H:%M")
            self.catalog_data['devicesList'].append(new_device)
            print("New device added successfully.")

    def print_all(self):
        for device in self.catalog_data['devicesList']:
            print(json.dumps(device, indent=4))

    def exit(self):
        self.save_catalog()


if __name__ == "__main__":
    catalog = DeviceCatalog("catalog.json")

    while True:
        print("\n1. Search by Name")
        print("2. Search by ID")
        print("3. Search by Service")
        print("4. Search by Measure Type")
        print("5. Insert Device")
        print("6. Print All Devices")
        print("7. Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            name = input("Enter device name: ")
            devices = catalog.search_by_name(name)
            for device in devices:
                print(json.dumps(device, indent=4))
        elif choice == "2":
            device_id = int(input("Enter device ID: "))
            device = catalog.search_by_id(device_id)
            if device:
                print(json.dumps(device, indent=4))
            else:
                print("Device not found.")
        elif choice == "3":
            service = input("Enter service: ")
            devices = catalog.search_by_service(service)
            for device in devices:
                print(json.dumps(device, indent=4))
        elif choice == "4":
            measure_type = input("Enter measure type: ")
            devices = catalog.search_by_measure_type(measure_type)
            for device in devices:
                print(json.dumps(device, indent=4))
        elif choice == "5":
            try:
                catalog.insert_device()
            except json.JSONDecodeError as e:
                print(e)
        elif choice == "6":
            catalog.print_all()
        elif choice == "7":
            print("Exiting...")
            catalog.exit()
            print("Catalog saved. \nExiting program...")
            break

