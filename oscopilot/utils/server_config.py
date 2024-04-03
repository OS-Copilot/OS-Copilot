import os

class ConfigManager:
    """
    A singleton class responsible for managing configuration settings across the application.

    This class implements the singleton design pattern to ensure that only one instance of the
    ConfigManager exists at any time. It provides methods to set, apply, and clear proxy settings
    for HTTP and HTTPS traffic.

    Attributes:
        _instance (ConfigManager): A private class-level attribute that holds the singleton instance.
        http_proxy (str): The HTTP proxy URL.
        https_proxy (str): The HTTPS proxy URL.
    """
    _instance = None

    def __new__(cls):
        """
        Overrides the default instantiation process to ensure only one instance of ConfigManager is created.

        Returns:
            ConfigManager: The singleton instance of the ConfigManager.
        """
        if cls._instance is None:
            cls._instance = super(ConfigManager, cls).__new__(cls)
            cls._instance.http_proxy = "http://127.0.0.1:10809"
            cls._instance.https_proxy = "http://127.0.0.1:10809"
            # cls._instance.http_proxy = None
            # cls._instance.https_proxy = None
        return cls._instance

    def set_proxies(self, http, https):
        """
        Sets the HTTP and HTTPS proxy URLs.

        Args:
            http (str): The HTTP proxy URL.
            https (str): The HTTPS proxy URL.
        """
        self.http_proxy = http
        self.https_proxy = https

    def apply_proxies(self):
        """
        Applies the configured proxy settings by setting them in the environments variables.

        The method sets the 'http_proxy' and 'https_proxy' environments variables based on the
        configured proxy URLs. If no proxies are configured, the environments variables are not modified.
        """
        if self.http_proxy:
            os.environ["http_proxy"] = self.http_proxy
        if self.https_proxy:
            os.environ["https_proxy"] = self.https_proxy

    def clear_proxies(self):
        """
        Clears the proxy settings from the environments variables.

        This method removes the 'http_proxy' and 'https_proxy' entries from the environments variables,
        effectively clearing any proxy settings that were previously applied.
        """
        os.environ.pop("http_proxy", None)
        os.environ.pop("https_proxy", None)

