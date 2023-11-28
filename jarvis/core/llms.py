import os
import openai
import time
import json

proxy = {
'http': 'http://localhost:2080',
'https': 'http://localhost:2080',
}


class OpenAI:
    """
    A wrapper for OpenAI API= self._client.send(request, auth=self.custom_auth, stream=stream)
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/wengzhenmin/anaconda3/envs/jarvis_env/lib/python3.11/site-packages/httpx/_client.py", line 901, in send
    response = self._send_handling_auth(
               ^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/wengzhenmin/anaconda3/envs/jarvis_env/lib/python3.11/site-packages/httpx/_client.py", line 929, in _send_handling_auth
    response = self._send_handling_redirects(
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/wengzhenmin/anaconda3/envs/jarvis_env/lib/python3.11/site-packages/httpx/_client.py", line 966, in _send_handling_redirects
    response = self._send_single_request(request)
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/wengzhenmin/anaconda3/envs/jarvis_env/lib/python3.11/site-packages/httpx/_client.py", line 1002, in _send_single_request
    response = transport.handle_request(request)
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/wengzhenmin/anaconda3/envs/jarvis_env/lib/python3.11/site-packages/httpx/_transports/default.py", line 227, in handle_request
    with map_httpcore_exceptions():
  File "/home/wengzhenmin/anaconda3/envs/jarvis_env/lib/python3.11/contextlib.py", line 155, in __exit__
    self.gen.throw(typ, value, traceback)
  File "/home/wengzhenmin/anaconda3/envs/jarvis_env/lib/python3.11/site-packages/httpx/_transports/default.py", line 83, in map_httpcore_exceptions
    raise mapped_exc(message) from exc
httpx.ConnectError: [Errno 101] Network is unreachable

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/home/wengzhenmin/anaconda3/envs/jarvis_env/lib/python3.11/site-packages/httpcore/_exceptions.py", line 10, in map_exceptions
    yield
  File "/home/wengzhenmin/anaconda3/envs/jarvis_env/lib/python3.11/site-packages/httpcore/_backends/sync.py", line 206, in connect_tcp
    sock = socket.create_connection(
           ^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/wengzhenmin/anaconda3/envs/jarvis_env/lib/python3.11/socket.py", line 851, in create_connection
    raise exceptions[0]
  File "/home/wengzhenmin/anaconda3/envs/jarvis_env/lib/python3.11/socket.py", line 836, in create_connection
    sock.connect(sa)
OSError: [Errno 101] Network is unreachable

The above exception was the direct cause of the following exception:

Traceback (most recent call last):
  File "/home/wengzhenmin/anaconda3/envs/jarvis_env/lib/python3.11/site-packages/httpx/_transports/default.py", line 66, in map_httpcore_exceptions
    yield
  File "/home/wengzhenmin/anaconda3/envs/jarvis_env/lib/python3.11/site-packages/httpx/_transports/default.py", line 228, in handle_request
    resp = self._pool.handle_request(req)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/wengzhenmin/anaconda3/envs/jarvis_env/lib/python3.11/site-packages/httpcore/_sync/connection_pool.py", line 268, in handle_request
    raise exc
  File "/home/wengzhenmin/anaconda3/envs/jarvis_env/lib/python3.11/site-packages/httpcore/_sync/connection_pool.py", line 251, in handle_request
    response = connection.handle_request(request)
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/wengzhenmin/anaconda3/envs/jarvis_env/lib/python3.11/site-packages/httpcore/_sync/connection.py", line 99, in handle_request
    raise exc
  File "/home/wengzhenmin/anaconda3/envs/jarvis_env/lib/python3.11/site-packages/httpcore/_sync/connection.py", line 76, in handle_request
    stream = self._connect(request)
             ^^^^^^^^^^^^^^^^^^^^^^
  File "/home/wengzhenmin/anaconda3/envs/jarvis_env/lib/python3.11/site-packages/httpcore/_sync/connection.py", line 124, in _connect
    stream = self._network_backend.connect_tcp(**kwargs)
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/wengzhenmin/anaconda3/envs/jarvis_env/lib/python3.11/site-packages/httpcore/_backends/sync.py", line 205, in connect_tcp
    with map_exceptions(exc_map):
  File "/home/wengzhenmin/anaconda3/envs/jarvis_env/lib/python3.11/contextlib.py", line 155, in __exit__
    self.gen.throw(typ, value, traceback)
  File "/home/wengzhenmin/anaconda3/envs/jarvis_env/lib/python3.11/site-packages/httpcore/_exceptions.py", line 14, in map_exceptions
    raise to_exc(exc) from exc
httpcore.ConnectError: [Errno 101] Network is unreachable

The above exception was the direct cause of the following exception:

Traceback (most recent call last):
  File "/home/wengzhenmin/anaconda3/envs/jarvis_env/lib/python3.11/site-packages/openai/_base_client.py", line 866, in _request
    response = self._client.send(request, auth=self.custom_auth, stream=stream)
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/wengzhenmin/anaconda3/envs/jarvis_env/lib/python3.11/site-packages/httpx/_client.py", line 901, in send
    response = self._send_handling_auth(
               ^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/wengzhenmin/anaconda3/envs/jarvis_env/lib/python3.11/site-packages/httpx/_client.py", line 929, in _send_handling_auth
    response = self._send_handling_redirects(
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/wengzhenmin/anaconda3/envs/jarvis_env/lib/python3.11/site-packages/httpx/_client.py", line 966, in _send_handling_redirects
    response = self._send_single_request(request)
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/wengzhenmin/anaconda3/envs/jarvis_env/lib/python3.11/site-packages/httpx/_client.py", line 1002, in _send_single_request
    response = transport.handle_request(request)
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/wengzhenmin/anaconda3/envs/jarvis_env/lib/python3.11/site-packages/httpx/_transports/default.py", line 227, in handle_request
    with map_httpcore_exceptions():
  File "/home/wengzhenmin/anaconda3/envs/jarvis_env/lib/python3.11/contextlib.py", line 155, in __exit__
    self.gen.throw(typ, value, traceback)
  File "/home/wengzhenmin/anaconda3/envs/jarvis_env/lib/python3.11/site-packages/httpx/_transports/default.py", line 83, in map_httpcore_exceptions
    raise mapped_exc(message) from exc
httpx.ConnectError: [Errno 101] Network is unreachable

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/home/wengzhenmin/anaconda3/envs/jarvis_env/lib/python3.11/site-packages/httpcore/_exceptions.py", line 10, in map_exceptions
    yield
  File "/home/wengzhenmin/anaconda3/envs/jarvis_env/lib/python3.11/site-packages/httpcore/_backends/sync.py", line 206, in connect_tcp
    sock = socket.create_connection(
           ^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/wengzhenmin/anaconda3/envs/jarvis_env/lib/python3.11/socket.py", line 851, in create_connection
    raise exceptions[0]
  File "/home/wengzhenmin/anaconda3/envs/jarvis_env/lib/python3.11/socket.py", line 836, in create_connection
    sock.connect(sa)
OSError: [Errno 101] Network is unreachable

The above exception was the direct cause of the following exception:

Traceback (most recent call last):
  File "/home/wengzhenmin/anaconda3/envs/jarvis_env/lib/python3.11/site-packages/httpx/_transports/default.py", line 66, in map_httpcore_exceptions
    yield
  File "/home/wengzhenmin/anaconda3/envs/jarvis_env/lib/python3.11/site-packages/httpx/_transports/default.py", line 228, in handle_request
    resp = self._pool.handle_request(req)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/wengzhenmin/anaconda3/envs/jarvis_env/lib/python3.11/site-packages/httpcore/_sync/connection_pool.py", line 268, in handle_request
    raise exc
  File "/home/wengzhenmin/anaconda3/envs/jarvis_env/lib/python3.11/site-packages/httpcore/_sync/connection_pool.py", line 251, in handle_request
    response = connection.handle_request(request)
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/wengzhenmin/anaconda3/envs/jarvis_env/lib/python3.11/site-packages/httpcore/_sync/connection.py", line 99, in handle_request
    raise exc
  File "/home/wengzhenmin/anaconda3/envs/jarvis_env/lib/python3.11/site-packages/httpcore/_sync/connection.py", line 76, in handle_request
    stream = self._connect(request)
             ^^^^^^^^^^^^^^^^^^^^^^
  File "/home/wengzhenmin/anaconda3/envs/jarvis_env/lib/python3.11/site-packages/httpcore/_sync/connection.py", line 124, in _connect
    stream = self._network_backend.connect_tcp(**kwargs)
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/wengzhenmin/anaconda3/envs/jarvis_env/lib/python3.11/site-packages/httpcore/_backends/sync.py", line 205, in connect_tcp
    with map_exceptions(exc_map):
  File "/home/wengzhenmin/anaconda3/envs/jarvis_env/lib/python3.11/contextlib.py", line 155, in __exit__
    self.gen.throw(typ, value, traceback)
  File "/home/wengzhenmin/anaconda3/envs/jarvis_env/lib/python3.11/site-packages/httpcore/_exceptions.py", line 14, in map_exceptions
    raise to_exc(exc) from exc
httpcore.ConnectError: [Errno 101] Network is unreachable

The above exception was the direct cause of the following exception:

Traceback (most recent call last):
  File "/home/wengzhenmin/anaconda3/envs/jarvis_env/lib/python3.11/site-packages/openai/_base_client.py", line 866, in _request
    response = self._client.send(request, auth=self.custom_auth, stream=stream)
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/wengzhenmin/anaconda3/envs/jarvis_env/lib/python3.11/site-packages/httpx/_client.py", line 901, in send
    response = self._send_handling_auth(
               ^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/wengzhenmin/anaconda3/envs/jarvis_env/lib/python3.11/site-packages/httpx/_client.py", line 929, in _send_handling_auth
    response = self._send_handling_redirects(
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/wengzhenmin/anaconda3/envs/jarvis_env/lib/python3.11/site-packages/httpx/_client.py", line 966, in _send_handling_redirects
    response = self._send_single_request(request)
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/wengzhenmin/anaconda3/envs/jarvis_env/lib/python3.11/site-packages/httpx/_client.py", line 1002, in _send_single_request
    response = transport.handle_request(request)
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/wengzhenmin/anaconda3/envs/jarvis_env/lib/python3.11/site-packages/httpx/_transports/default.py", line 227, in handle_request
    with map_httpcore_exceptions():
  File "/home/wengzhenmin/anaconda3/envs/jarvis_env/lib/python3.11/contextlib.py", line 155, in __exit__
    self.gen.throw(typ, value, traceback)
  File "/home/wengzhenmin/anaconda3/envs/jarvis_env/lib/python3.11/site-packages/httpx/_transports/default.py", line 83, in map_httpcore_exceptions
    raise mapped_exc(message) from exc
httpx.ConnectError: [Errno 101] Network is unreachable

The above exception was the direct cause of the following exception:

Traceback (most recent call last):
  File "/home/wengzhenmin/Projects/jarvis/jarvis/agent/linux_invoke_generator.py", line 130, in <module>
    res = test.invoke_generator(class_code, task_description)
          ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/wengzhenmin/Projects/jarvis/jarvis/agent/linux_invoke_generator.py", line 54, in invoke_generator
    return self.llm.chat(self.message)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/wengzhenmin/Projects/jarvis/jarvis/core/llms.py", line 25, in chat
    response = openai.chat.completions.create(
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/wengzhenmin/anaconda3/envs/jarvis_env/lib/python3.11/site-packages/openai/_utils/_utils.py", line 299, in wrapper
    return func(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^
  File "/home/wengzhenmin/anaconda3/envs/jarvis_env/lib/python3.11/site-packages/openai/resources/chat/completions.py", line 598, in create
    return self._post(
           ^^^^^^^^^^^
  File "/home/wengzhenmin/anaconda3/envs/jarvis_env/lib/python3.11/site-packages/openai/_base_client.py", line 1063, in post
    return cast(ResponseT, self.request(cast_to, opts, stream=stream, stream_cls=stream_cls))
                           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/wengzhenmin/anaconda3/envs/jarvis_env/lib/python3.11/site-packages/openai/_base_client.py", line 842, in request
    return self._request(
           ^^^^^^^^^^^^^^
  File "/home/wengzhenmin/anaconda3/envs/jarvis_env/lib/python3.11/site-packages/openai/_base_client.py", line 898, in _request
    return self._retry_request(
           ^^^^^^^^^^^^^^^^^^^^
  File "/home/wengzhenmin/anaconda3/envs/jarvis_env/lib/python3.11/site-packages/openai/_base_client.py", line 933, in _retry_request
    return self._request(
           ^^^^^^^^^^^^^^
  File "/home/wengzhenmin/anaconda3/envs/jarvis_env/lib/python3.11/site-packages/openai/_base_client.py", line 898, in _request
    return self._retry_request(
           ^^^^^^^^^^^^^^^^^^^^
  File "/home/wengzhenmin/anaconda3/envs/jarvis_env/lib/python3.11/site-packages/openai/_base_client.py", line 933, in _retry_request
    return self._request(
           ^^^^^^^^^^^^^^
  File "/home/wengzhenmin/anaconda3/envs/jarvis_env/lib/python3.11/site-packages/openai/_base_client.py", line 905, in _request
    raise APIConnectionError(request=request) from err
openai.APIConnectionError: Connection error.
    """
    def __init__(self, config_path=None):
        with open(config_path) as f:
            config = json.load(f)
        self.model_name = config['model_name']
        openai.api_key = config['OPENAI_API_KEY']
        openai.organization = config['OPENAI_ORGANIZATION']
        openai.proxy = proxy

    def chat(self, messages, temperature=0, sleep_time=2):
        response = openai.chat.completions.create(
            model=self.model_name,
            messages=messages,
            temperature=temperature
        )
        # time.sleep(sleep_time)
        # return response['choices'][0]['message']
        return response.choices[0].message.content


