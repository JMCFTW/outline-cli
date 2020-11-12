import json

import requests
from requests_toolbelt.adapters.fingerprint import FingerprintAdapter

from outline_cli.helper import (
    get_email_list_from_file,
    get_username_by_email,
    send_email,
)


class OutlineVPN:
    def __init__(self, certSha256="", apiUrl=""):
        self.certSha256 = certSha256
        self.apiUrl = apiUrl
        self.__init_requests_session()

    def __init_requests_session(self):
        self.session = requests.Session()
        self.session.mount(self.apiUrl, FingerprintAdapter(self.certSha256))

    def __call_api(self, api_path, request_method, request_body):
        response = self.session.request(
            method=request_method,
            url=(self.apiUrl + api_path),
            data=request_body,
            verify=False,
        )
        return response.text

    def get_server_info(self):
        return self.__call_api("/server", "GET", {})

    def change_hostname_for_access_keys(self, hostname):
        return self.__call_api(
            "/server/hostname-for-access-keys", "PUT", {"hostname": hostname}
        )

    def rename_server(self, name):
        return self.__call_api("/name", "PUT", {"name": name})

    def get_whether_metrics_is_being_shared(self):
        return self.__call_api("/metrics/enabled", "GET", {})

    def enable_or_disable_sharing_metrics(self, metricsEnabled):
        return self.__call_api(
            "/metrics/enabled", "PUT", {"metricsEnabled": metricsEnabled}
        )

    def change_default_port_for_newly_created_access(self, port):
        return self.__call_api(
            "/server/port-for-new-access-keys", "PUT", {"port": port}
        )

    def create_access_key(self):
        return self.__call_api("/access-keys", "POST", {})

    def list_access_keys(self):
        return self.__call_api("/access-keys", "GET", {})

    def delete_access_key(self, id):
        return self.__call_api(f"/access-keys/{id}", "DELETE", {})

    def rename_access_key(self, id, username):
        return self.__call_api(f"/access-keys/{id}/name", "PUT", {"name": username})

    def get_each_access_key_data_transferred(self):
        return self.__call_api("/metrics/transfer", "GET", {})

    def set_data_transfer_limit_for_all_access_keys(self, byte):
        return self.__call_api(
            "/experimental/access-key-data-limit", "PUT", {"limit": {"bytes": byte}}
        )

    def remove_access_key_data_limit(self):
        return self.__call_api("/experimental/access-key-data-limit", "DELETE", {})

    def create_user_by_email(self, email):
        username = get_username_by_email(email)
        resp = json.loads(self.create_access_key())
        self.rename_access_key(resp["id"], username)
        send_email(email, username, resp["accessUrl"])
        return resp

    def batch_create_user_by_email_list(self, email_list_filename):
        email_list = get_email_list_from_file(email_list_filename)
        for email in email_list:
            self.create_user_by_email(email)
        return "Finish"
