"""Module for configuration management"""
import configparser
import dataclasses
import os


@dataclasses.dataclass
class Config():
    """
    Represents the configuration options for this app
    """
    hosted_zone_id: str
    hosted_zone_name: str
    cognito_custom_domain: str
    application_dns_name: str
    backend_desired_count: int

def get_config(path_to_config: str = None) -> Config:
    """
    Returns an instance of the Config class based on reading
    either the default configuration or a config from
    path_to_config if that is supplied.

    :param path_to_config: Storage path of the configuration, defaults to None
    :type path_to_config: str, optional
    :return: Instance of Config
    :rtype: Config
    """

    path_to_config = os.path.join(
        os.path.dirname(__file__),
        "..",
        "configuration.ini"
    )

    cfg = configparser.ConfigParser()
    cfg.read(path_to_config)

    return Config(**cfg["main"])
