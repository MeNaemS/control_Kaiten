from schemas.settings_schemas import ConfigSchema
from dynaconf import Dynaconf
from dotenv import load_dotenv
from os import getenv


def get_settings(path_to_env: str, **kwargs) -> ConfigSchema:
    """
    Reading configs, at specified paths from env files.
    Args::
        :path_to_env — absolute or relative path to the file with environment variables.
    Kwargs::
        :named arguments for Dynaconf
    """
    if not load_dotenv(path_to_env):
        raise RuntimeError('Could not find the specified file.')
    return Dynaconf(
        envvar_prefix="DYNACONF",
        settings_files=[
            getenv('CONFIG'),
            getenv('SECRET')
        ],
        **kwargs
    )


config: ConfigSchema = get_settings('.env')
