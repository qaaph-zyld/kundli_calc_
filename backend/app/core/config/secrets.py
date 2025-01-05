"""Secrets management module using HashiCorp Vault."""
import hvac
from typing import Optional, Dict, Any
import os
from functools import lru_cache

class SecretsManager:
    """Secrets manager using HashiCorp Vault."""

    def __init__(self):
        self.client = self._init_vault_client()
        self._cache = {}

    def _init_vault_client(self) -> hvac.Client:
        """Initialize Vault client."""
        vault_url = os.getenv("VAULT_URL", "http://vault:8200")
        vault_token = os.getenv("VAULT_TOKEN")
        
        if not vault_token and not os.getenv("VAULT_ROLE_ID"):
            # Development mode - return None
            return None
            
        if vault_token:
            return hvac.Client(
                url=vault_url,
                token=vault_token
            )
        else:
            # Use AppRole authentication
            client = hvac.Client(url=vault_url)
            role_id = os.getenv("VAULT_ROLE_ID")
            secret_id = os.getenv("VAULT_SECRET_ID")
            
            resp = client.auth.approle.login(
                role_id=role_id,
                secret_id=secret_id
            )
            client.token = resp["auth"]["client_token"]
            return client

    def get_secret(self, path: str, key: Optional[str] = None) -> Any:
        """Get secret from Vault."""
        if path in self._cache:
            secret_data = self._cache[path]
        else:
            if not self.client:
                # Development mode - return dummy secrets
                secret_data = self._get_development_secrets(path)
            else:
                try:
                    secret = self.client.secrets.kv.v2.read_secret_version(
                        path=path
                    )
                    secret_data = secret["data"]["data"]
                    self._cache[path] = secret_data
                except Exception as e:
                    raise ValueError(f"Failed to get secret at path {path}: {str(e)}")

        if key:
            if key not in secret_data:
                raise ValueError(f"Key {key} not found in secret at path {path}")
            return secret_data[key]
        return secret_data

    def _get_development_secrets(self, path: str) -> Dict[str, str]:
        """Get development secrets."""
        dev_secrets = {
            "kundli/database": {
                "mongodb_url": "mongodb://localhost:27017",
                "redis_url": "redis://localhost:6379/0"
            },
            "kundli/jwt": {
                "secret_key": "dev-secret-key-never-use-in-production",
                "algorithm": "HS256"
            },
            "kundli/ssl": {
                "cert_path": "/etc/ssl/certs/dummy.crt",
                "key_path": "/etc/ssl/private/dummy.key"
            }
        }
        return dev_secrets.get(path, {})

@lru_cache()
def get_secrets_manager() -> SecretsManager:
    """Get cached secrets manager instance."""
    return SecretsManager()

# Create global instance
secrets = get_secrets_manager()
