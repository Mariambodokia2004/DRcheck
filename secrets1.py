from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient
import azure.core.exceptions
import os

def key_value_to_env():
    credentials = DefaultAzureCredential()

    key_vault_name = "prod-monitoring-kv"
    vault_url = f"https://{key_vault_name}.vault.azure.net"
    secret_list = ["NOC-DR-Automation-UserName", "NOC-DR-Automation-UserPassword"]

    try:
        secret_client = SecretClient(vault_url, credentials)
        for secret in secret_list:
            os.environ[secret] = secret_client.get_secret(secret).value
            # print(os.environ[secret])

    except azure.core.exceptions.ClientAuthenticationError as ex:
        response = f"Cannot connect to Azure , The error is: \n {ex}"
        return response
    except azure.core.exceptions.ResourceNotFoundError as ex:
        response = f"Error SecretNotFound: \n{ex.message}"
        return response

    except azure.core.exceptions.HttpResponseError as ex:
        if ex.reason == "Unauthorized":
            if ex.reason == "Unauthorized":
                response = f"Unauthorized error :\n {ex.message}"
                return response
            return ex.message
        

key_value_to_env()