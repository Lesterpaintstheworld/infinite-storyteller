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

    def input_image_to_chatgpt(self, asset_name):
        import requests
        import json
        
        image_data = self.get_image_for_llm(asset_name)
        
        # Replace with your actual API endpoint and key
        api_endpoint = "https://api.openai.com/v1/chat/completions"
        api_key = "your_openai_api_key_here"
        
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}"
        }
        
        payload = {
            "model": "gpt-4-vision-preview",
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": "Please provide a detailed description of this image."
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{image_data['image']}"
                            }
                        }
                    ]
                }
            ],
            "max_tokens": 300
        }
        
        response = requests.post(api_endpoint, headers=headers, data=json.dumps(payload))
        
        if response.status_code == 200:
            description = response.json()['choices'][0]['message']['content']
            self.add_image_description(asset_name, description)
            return description
        else:
            raise Exception(f"Error in API call: {response.status_code} - {response.text}")

    def add_image_description(self, asset_name, description):
        import json
        import os
        
        descriptions_file = os.path.join(self.asset_directory, 'image_descriptions.json')
        
        if os.path.exists(descriptions_file):
            with open(descriptions_file, 'r') as f:
                descriptions = json.load(f)
        else:
            descriptions = {}
        
        descriptions[asset_name] = description
        
        with open(descriptions_file, 'w') as f:
            json.dump(descriptions, f, indent=2)

# Example usage:
# asset_manager = AssetManager('path/to/assets')
# asset_manager.add_asset('images', 'city_skyline', 'path/to/skyline.jpg', {'author': 'Lesterpaintstheworld', 'description': 'Futuristic city skyline'})
# description = asset_manager.input_image_to_chatgpt('city_skyline')
# print(description)
