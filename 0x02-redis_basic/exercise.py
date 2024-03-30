#!/usr/bin/env python3
""" Cache class """
import uuid
import redis
from functools import wraps
from typing import Any, Callable, Union


def count_calls(method: Callable) -> Callable:
    """ count number of times a method is called """
    @wraps(method)
    def invoker(self, *args, **kwargs) -> Any:
        """ increases the count by one """
        if isinstance(self._redis, redis.Redis):
            self._redis.incr(method.__qualname__)
        return method(self, *args, **kwargs)
    return invoker


def call_history(method: Callable) -> Callable:
    """ history of calls to a method """

    # Define inputs and outputs lists keys
    input_keys = method.__qualname__ + ':inputs'
    output_keys = method.__qualname__ + ':outputs'

    @wraps(method)
    def invoker(self, *args, **kwargs) -> Any:
        """ Returns method's output after storing """

        self.rpush(input_keys, str(args))
        outs = method(self, *args, **kwargs)
        self.rpush(output_keys, outs)

        return outs
    return invoker


def replay(method: Callable) -> None:
    """ Display the history of calls of a particular function """

    history_str = ''
    redis_inst = redis.Redis()

    method_called = method.__qualname__
    input_keys = method.__qualname__ + ':inputs'
    output_keys = method.__qualname__ + ':outputs'

    count = redis_inst.get(method_called)

    if not count:
        print(f'{method_called} was called 0 times')

    history_str += f'{method_called} was called {int(count)} times:\n'

    inputs = redis_inst.lrange(input_keys, 0, -1)
    outputs = redis_inst.lrange(output_keys, 0, -1)

    for inp, outp in zip(inputs, outputs):
        history_str += f"{method_called}(*{inp.decode()}) -> {outp.decode()}\n"

    print(history_str, end='')


class Cashe:
    """ Redis Data Storage """

    def __init__(self) -> None:
        """ create a redis instance and flush it """
        self._redis = redis.Redis()
        self._redis.flushdb()

    @call_history
    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """ Create a key, store data in Redis using the 
        random key and return the key
        """

        data_key = str(uuid.uuid4())
        self._redis.set(data_key, data)

        return data_key

    def get(self, key: str, fn: callable = None) -> Any:
        """ return the key's stored value """

        value_data = self._redis.get(key)

        return value_data if not fn else fn(value_data)

    def get_str(self, key: str) -> Union[str, None]:
        """ Get string value stored in key """
        return self.get(key, str)

    def get_int(self, key: str) -> Union[int, None]:
        """ Get integer value stored in key """
        return self.get(key, int)
