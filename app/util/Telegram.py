from app.util.DotDict import DotDict
import time
import telegram.client as client
from app.config.config import Config
import os
import concurrent.futures
import threading


class Telegram:
    def __init__(
            self,
            api_id,
            api_hash,
            phone,
            database_encryption_key,
            tdlib_directory,
            proxy_server=None,
            proxy_port=None,
            proxy_secret=None
    ):
        if (proxy_server):
            self.tg = client.Telegram(
                api_id=api_id,
                api_hash=api_hash,
                phone=phone,
                database_encryption_key=database_encryption_key,
                files_directory=tdlib_directory,
                proxy_server=proxy_server,
                proxy_port=proxy_port,
                proxy_type={
                    '@type': 'proxyTypeMtproto',
                    'secret': proxy_secret
                }
            )
        else:
            self.tg = client.Telegram(
                api_id=api_id,
                api_hash=api_hash,
                phone=phone,
                database_encryption_key=database_encryption_key,
                files_directory=tdlib_directory,
            )
        self.tg.login()

    def __del__(self):
        self.tg.stop()

    def _call(self, method_name, params):
        result = self.tg.call_method(
            method_name=method_name,
            params=params
        )
        result.wait()
        return result

    def _dot(self, dict):
        return DotDict(dict)

    def set_log_verbose_level(self, new_verbosity_level):
        # level 0: fatal errors
        # level 1: erroes
        # level 2: warning & debug
        # level 3: info
        # level 4: debug
        # level 5: verbose debu
        result = self._call("setLogVerbosityLevel", {
            'new_verbosity_level': new_verbosity_level
        })
        return result

    def download_file(self, file_id, priority):
        result = self._call("downloadFile", {
            'file_id': file_id,
            'priority': priority,
            'synchronous': True
        })
        return result

    def cancel_download_file(self, file_id, only_if_pending):
        result = self._call("cancelDownloadFile", {
            'file_id': file_id,
            'only_if_pending': only_if_pending,
        })
        return result

    def speed_test(self, file_id):
        result = None
        start_time = time.time()

        with concurrent.futures.ThreadPoolExecutor() as executor:
            future = executor.submit(lambda: self.download_file(file_id, 32))
            try:
                result = future.result(timeout=Config.download_timeout)
            except concurrent.futures.TimeoutError:
                self.cancel_download_file(file_id, False)
                # todo we need to remove download
                return 0
        end_time = time.time()
        elapsed_time = end_time - start_time
        file_path = result.update['local']['path']
        size = result.update['size']
        if os.path.exists(file_path):
            os.remove(file_path)
        return round(size / elapsed_time / 1000, 2)

    def add_proxy(self, server, port, secret):
        return self._call("addProxy", {
            'server': server,
            'port': port,
            'enable': True,
            'type': {
                '@type': 'proxyTypeMtproto',
                'secret': secret
            }
        })

    def enable_proxy(self, proxy_id):
        return self._call("enableProxy", {
            'proxy_id': proxy_id
        })

    def remove_proxy(self, proxy_id):
        return self._call("removeProxy", {
            'proxy_id': proxy_id
        })

    def ping_proxy(self, proxy_id):
        return self._call("pingProxy", {
            'proxy_id': proxy_id
        })

    def get_proxies(self):
        result = self._call("getProxies", {})
        proxies = result.update['proxies']
        output = []
        for proxy in proxies:
            output.append(self._dot(proxy))
        return output

    def remove_all_proxies(self):
        proxies = self.get_proxies()
        for proxy in proxies:
            self.remove_proxy(proxy.id)

    def search_public_chat(self, username):
        result = self._call("searchPublicChat", {
            'username': username
        })
        return result.update['id']

    def get_message(self, chat_id, message_id):
        return self._call("getMessage", {
            'chat_id': chat_id,
            'message_id': message_id
        })

    def get_chat_history(self, chat_id, limit, from_message_id, offset, only_local):
        result = self._call("getChatHistory", {
            'chat_id': chat_id,
            'limit': limit,
            'from_message_id': from_message_id,
            'offset': offset,
            'only_local': only_local,
        })
        return result

    def channel_history(self, chat_id, limit, min_message_id):
        last_message_id = None
        from_message_id = 0
        counter = 0
        recived_messages = []
        flag = True
        while (flag):
            result = self.get_chat_history(
                chat_id, 50, from_message_id, 0, False)
            if (result.error):
                raise Exception(
                    f"Error happend in fetch channel_history, chat_id {chat_id} " + str(result.error_info['message']))
            if (result.update['total_count'] == 0):
                break
            for message in result.update['messages']:
                counter += 1
                message_id = message['id']
                from_message_id = message_id
                if (min_message_id and message_id <= min_message_id):
                    flag = False
                    break
                if (not last_message_id):
                    last_message_id = message_id
                recived_messages.append(message)
                if counter >= limit:
                    flag = False
                    break
        if (not last_message_id and min_message_id):
            last_message_id = min_message_id
        return recived_messages, last_message_id

    def idle(self):
        self.tg.idle()

    def stop(self):
        self.tg.stop()
