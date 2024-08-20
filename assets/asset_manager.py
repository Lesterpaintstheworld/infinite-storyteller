import os
import json
import base64
from PIL import Image
import io

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

    def encode_image_to_base64(self, asset_name):
        asset_info = self.get_asset('images', asset_name)
        if asset_info is None:
            raise ValueError(f"Image not found: {asset_name}")
        
        image_path = asset_info['file_path']
        with Image.open(image_path) as img:
            # Convert image to RGB mode if it's not
            if img.mode != 'RGB':
                img = img.convert('RGB')
            
            # Resize image if it's too large (optional)
            max_size = (1024, 1024)  # You can adjust this
            img.thumbnail(max_size, Image.LANCZOS)
            
            # Save image to bytes
            buffered = io.BytesIO()
            img.save(buffered, format="JPEG")
        
        # Encode the image
        img_str = base64.b64encode(buffered.getvalue()).decode()
        return f"data:image/jpeg;base64,{img_str}"

    def get_image_for_llm(self, asset_name):
        base64_image = self.encode_image_to_base64(asset_name)
        asset_info = self.get_asset('images', asset_name)
        return {
            'image': base64_image,
            'metadata': asset_info['metadata']
        }

# Example usage:
# asset_manager = AssetManager('path/to/assets')
# asset_manager.add_asset('images', 'city_skyline', 'path/to/skyline.jpg', {'author': 'Lesterpaintstheworld', 'description': 'Futuristic city skyline'})
# image_data = asset_manager.get_image_for_llm('city_skyline')
# print(image_data['metadata'])
# print(image_data['image'][:100])  # Print first 100 characters of base64 string
