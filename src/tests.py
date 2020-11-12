import unittest
from unittest.mock import MagicMock, patch

from requests.exceptions import MissingSchema

import outline_cli
from outline_cli.gmail import Gmail
from outline_cli.helper import (
    get_config_from_app_ini,
    get_email_list_from_file,
    get_username_by_email,
    send_email,
)
from outline_cli.outline import OutlineVPN


class TestOutlineVPN(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.client = OutlineVPN("test_certSha256", "https://test_apiUrl")

    @patch.object(OutlineVPN, "_OutlineVPN__call_api")
    def test_get_server_info(self, mock):
        mock.return_value = "ok"
        self.client.get_server_info()
        mock.assert_called_once_with("/server", "GET", {})

    @patch.object(OutlineVPN, "_OutlineVPN__call_api")
    def test_create_access_key(self, mock):
        mock.return_value = "ok"
        self.client.create_access_key()
        mock.assert_called_once_with("/access-keys", "POST", {})

    @patch.object(OutlineVPN, "_OutlineVPN__call_api")
    def test_list_access_keys(self, mock):
        mock.return_value = "ok"
        self.client.list_access_keys()
        mock.assert_called_once_with("/access-keys", "GET", {})

    @patch.object(OutlineVPN, "_OutlineVPN__call_api")
    def test_delete_access_key(self, mock):
        mock.return_value = "ok"
        self.client.delete_access_key(id=1)
        mock.assert_called_once_with("/access-keys/1", "DELETE", {})

    @patch.object(OutlineVPN, "_OutlineVPN__call_api")
    def test_rename_access_key(self, mock):
        mock.return_value = "ok"
        self.client.rename_access_key(id=1, username="Jimmy Chen")
        mock.assert_called_once_with(
            "/access-keys/1/name", "PUT", {"name": "Jimmy Chen"}
        )

    @patch.object(OutlineVPN, "_OutlineVPN__call_api")
    def test_get_each_access_key_data_transferred(self, mock):
        mock.return_value = "ok"
        self.client.get_each_access_key_data_transferred()
        mock.assert_called_once_with("/metrics/transfer", "GET", {})

    @patch.object(OutlineVPN, "_OutlineVPN__call_api")
    @patch("outline_cli.outline.send_email")
    def test_create_user_by_email(self, send_email_mock, outline_mock):
        outline_mock.return_value = '{"id": 1, "accessUrl": 1}'
        send_email_mock.return_value = "Success"
        self.client.create_user_by_email("test.chen@gmail.com")
        assert outline_mock.call_count == 2
        assert send_email_mock.call_count == 1

    @patch.object(OutlineVPN, "_OutlineVPN__call_api")
    def test_change_hostname_for_access_keys(self, mock):
        mock.return_value = "ok"
        self.client.change_hostname_for_access_keys("127.0.0.1")
        mock.assert_called_once_with(
            "/server/hostname-for-access-keys", "PUT", {"hostname": "127.0.0.1"}
        )

    @patch.object(OutlineVPN, "_OutlineVPN__call_api")
    def test_rename_server(self, mock):
        mock.return_value = "ok"
        self.client.rename_server("test server")
        mock.assert_called_once_with("/name", "PUT", {"name": "test server"})

    @patch.object(OutlineVPN, "_OutlineVPN__call_api")
    def test_get_whether_metrics_is_being_shared(self, mock):
        mock.return_value = "ok"
        self.client.get_whether_metrics_is_being_shared()
        mock.assert_called_once_with("/metrics/enabled", "GET", {})

    @patch.object(OutlineVPN, "_OutlineVPN__call_api")
    def test_enable_or_disable_sharing_metrics(self, mock):
        mock.return_value = "ok"
        self.client.enable_or_disable_sharing_metrics(True)
        mock.assert_called_once_with(
            "/metrics/enabled", "PUT", {"metricsEnabled": True}
        )

    @patch.object(OutlineVPN, "_OutlineVPN__call_api")
    def test_change_default_port_for_newly_created_access(self, mock):
        mock.return_value = "ok"
        self.client.change_default_port_for_newly_created_access("7004")
        mock.assert_called_once_with(
            "/server/port-for-new-access-keys", "PUT", {"port": "7004"}
        )

    @patch.object(OutlineVPN, "_OutlineVPN__call_api")
    def test_set_data_transfer_limit_for_all_access_keys(self, mock):
        mock.return_value = "ok"
        self.client.set_data_transfer_limit_for_all_access_keys(1234)
        mock.assert_called_once_with(
            "/experimental/access-key-data-limit", "PUT", {"limit": {"bytes": 1234}}
        )

    @patch.object(OutlineVPN, "_OutlineVPN__call_api")
    def test_remove_access_key_data_limit(self, mock):
        mock.return_value = "ok"
        self.client.remove_access_key_data_limit()
        mock.assert_called_once_with(
            "/experimental/access-key-data-limit", "DELETE", {}
        )

    @patch.object(OutlineVPN, "_OutlineVPN__call_api")
    @patch("outline_cli.outline.send_email")
    def test_batch_create_user_by_email_list(self, send_email_mock, outline_mock):
        outline_mock.return_value = '{"id": 1, "accessUrl": 1}'
        send_email_mock.return_value = "Success"
        self.client.batch_create_user_by_email_list("example_email_list.txt")
        assert outline_mock.call_count == 20
        assert send_email_mock.call_count == 10


class TestHelper(unittest.TestCase):
    def test_get_config_from_app_ini(self):
        assert get_config_from_app_ini("Gmail", "EMAIL") == "your_email"

    def test_get_email_list_from_file(self):
        assert get_email_list_from_file("example_email_list.txt") == [
            "user1@gmail.com",
            "user2@gmail.com",
            "user3@gmail.com",
            "user4@gmail.com",
            "user5@gmail.com",
            "user6@gmail.com",
            "user7@gmail.com",
            "user8@gmail.com",
            "user9@gmail.com",
            "user10@gmail.com",
        ]

    def test_get_username_by_email(self):
        assert get_username_by_email("jimmy.chen@gmail.com") == "Jimmy Chen"

    @patch("outline_cli.helper.Gmail")
    def test_send_email(self, mock):
        mock.init_server = MagicMock()
        mock.send = MagicMock()
        send_email(
            "jimmy.chen@gmail.com", "Jimmy Chen", {"accessUrl": "test accessUrl"}
        )


class TestGmail(unittest.TestCase):
    @patch.object(Gmail, "_Gmail__login")
    def test_gmail(self, mock):
        server = Gmail("user", "password")
        server.send = MagicMock()
        server.send("Hello world")
        server.quit()


class TestMain(unittest.TestCase):
    def test_init_outline(self):
        outline_cli.init_outline()

    @patch("outline_cli.prompt")
    def test_main(self, mock):
        mock.return_value = {"method": "batch_create_user_by_email_list"}
        try:
            outline_cli.init_cli()
        except (MissingSchema, TypeError):
            pass

    @patch("outline_cli.prompt")
    def test_main2(self, mock):
        mock.return_value = {"method": "get_server_info"}
        try:
            outline_cli.init_cli()
        except MissingSchema:
            pass
