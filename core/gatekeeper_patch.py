import os
import json

class Gatekeeper:
    _registry_cache = {}
    _blacklist_cache = {}

    def __init__(self, registry_path='core/registry/networks.json', blacklist_path='core/registry/blacklist.json'):
        # Carregar Registry Local (Para Wallets e regras fixas)
        if registry_path in self._registry_cache:
            self.registry = self._registry_cache[registry_path]
        else:
            if os.path.exists(registry_path):
                with open(registry_path, 'r') as f:
                    self.registry = json.load(f)
            else:
                self.registry = {"wallets": {}, "exchanges": {}}
            self._registry_cache[registry_path] = self.registry

        # Carregar Blacklist
        if blacklist_path in self._blacklist_cache:
            self.blacklist = self._blacklist_cache[blacklist_path]
        else:
            if os.path.exists(blacklist_path):
                with open(blacklist_path, 'r') as f:
                    self.blacklist = json.load(f)
            else:
                self.blacklist = []
            self._blacklist_cache[blacklist_path] = self.blacklist
