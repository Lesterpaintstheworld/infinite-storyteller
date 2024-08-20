import os
import json

class AssetManager:
    def __init__(self, asset_directory):
        self.asset_directory = asset_directory
        self.asset_catalog = {}
        self.load_asset_catalog()

    def load_asset_catalog(self):
        catalog_path = os.path.join(self.asset_directory, 'asset_catalog.json')
        if os.path.exists(catalog_path):
            with open(catalog_path, 'r') as f:
                self.asset_catalog = json.load(f)
        else:
            self.asset_catalog = {
                'images': {},
                'audio': {},
                '3d_models': {}
            }

    def save_asset_catalog(self):
        catalog_path = os.path.join(self.asset_directory, 'asset_catalog.json')
        with open(catalog_path, 'w') as f:
            json.dump(self.asset_catalog, f, indent=2)

    def add_asset(self, asset_type, asset_name, file_path, metadata=None):
        if asset_type not in self.asset_catalog:
            raise ValueError(f"Invalid asset type: {asset_type}")

        relative_path = os.path.relpath(file_path, self.asset_directory)
        self.asset_catalog[asset_type][asset_name] = {
            'file_path': relative_path,
            'metadata': metadata or {}
        }
        self.save_asset_catalog()

    def get_asset(self, asset_type, asset_name):
        if asset_type not in self.asset_catalog or asset_name not in self.asset_catalog[asset_type]:
            return None
        asset_info = self.asset_catalog[asset_type][asset_name]
        full_path = os.path.join(self.asset_directory, asset_info['file_path'])
        return {
            'file_path': full_path,
            'metadata': asset_info['metadata']
        }

    def list_assets(self, asset_type=None):
        if asset_type:
            return list(self.asset_catalog.get(asset_type, {}).keys())
        return {k: list(v.keys()) for k, v in self.asset_catalog.items()}

    def update_asset_metadata(self, asset_type, asset_name, metadata):
        if asset_type in self.asset_catalog and asset_name in self.asset_catalog[asset_type]:
            self.asset_catalog[asset_type][asset_name]['metadata'].update(metadata)
            self.save_asset_catalog()
        else:
            raise ValueError(f"Asset not found: {asset_type}/{asset_name}")

# Example usage:
# asset_manager = AssetManager('path/to/assets')
# asset_manager.add_asset('images', 'city_skyline', 'path/to/skyline.jpg', {'author': 'Lesterpaintstheworld', 'description': 'Futuristic city skyline'})
# asset_info = asset_manager.get_asset('images', 'city_skyline')
# print(asset_info)
