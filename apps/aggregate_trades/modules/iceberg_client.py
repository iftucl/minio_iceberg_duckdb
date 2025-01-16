from pyiceberg.catalog import load_catalog

class IcebergClient:
    def __init__(self, ice_host_uri: str, ice_api: str, username: str, password: str, app_name: str):
        self.ice_host_uri = ice_host_uri
        self.ice_api = ice_api
        self.user_name = username
        self.password = password
        self.app_name = app_name
        self.catalog = self._get_catolog()
    def _get_catalog(self):
        catalog = load_catalog(
            self.app_name,
            **{
                "uri": self.ice_api,
                "s3.endpoint": self.ice_host_uri,
                "s3.access-key-id": self.user_name,
                "s3.secret-access-key": self.password,
            }
        )
        return catalog
