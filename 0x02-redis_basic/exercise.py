#!/usr/bin/env python3
""" A Cache class that store an instance of the Redis client."""
import redis
import uuid
from typing import Union, Callable, Optional
import functools


def call_history(method: Callable) -> Callable:
    """
    Decorator that stores the history of inputs and
    outputs for a method in Redis lists.
    """
    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        # Prepare Redis keys for inputs and outputs
        key_inputs = method.__qualname__ + ":inputs"
        key_outputs = method.__qualname__ + ":outputs"

        # Store input arguments as a normalized string
        input_str = str(args)
        self._redis.rpush(key_inputs, input_str)

        # Execute the original method to get the output
        output = method(self, *args, **kwargs)

        # Store the output in Redis
        self._redis.rpush(key_outputs, str(output))

        return output

    return wrapper


def count_calls(method: Callable) -> Callable:
    """
    Decorator that counts the number of calls to a method.
    The count is stored in Redis using the method's qualified name as the key.
    """
    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        # Increment the count in Redis
        key = method.__qualname__
        self._redis.incr(key)
        # Call the original method and return its result
        return method(self, *args, **kwargs)
    return wrapper


class Cache:
    """ Class Cache."""
    def __init__(self):
        """ Init method creates a new Redis client instance using redis.Redis()
        and stores it as a private variable and clears the entire Redis databas
        using flushdb()
        """
        self._redis = redis.Redis()
        self._redis.flushdb()

    @call_history
    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """ Method takes a data arg and returns a string.
        It generates a random key using uuid and store the input data in Redis
        using the random key and return the key.
        """
        key = str(uuid.uuid4())
        if isinstance(data, (int, float)):
            self._redis.set(key, str(data))
        else:
            self._redis.set(key, data)
        return key

    def get(
            self, key: str, fn: Optional[Callable[[bytes], Union[
                str, int, float]]] = None) -> Optional[Union[str, int, float]]:
        """
        Retrieves the data stored under the given key from the Redis cache.

        Args:
            key (str): The key of the data to be retrieved.
            fn (Optional[Callable[[bytes], Union[str, int, float]]]):
            An optional function to convert the retrieved data to the
            desired format.

        Returns:
            Optional[Union[str, int, float]]: The retrieved data, converted
            using the provided function if specified,
            or None if the key does not exist.
        """
        value = self._redis.get(key)
        if value is None:
            return None
        if fn is None:
            return value
        else:
            try:
                return fn(value)
            except Exception:
                raise ValueError(
                        "Error converting value using the provided callable")

    def get_str(self, key: str) -> Optional[str]:
        """
        Retrieves the data stored under the given key as a string.

        Args:
            key (str): The key of the data to be retrieved.

        Returns:
            Optional[str]: The retrieved data as a string,
            or None if the key does not exist.
        """
        return self.get(key, lambda x: x.decode())

    def get_int(self, key: str) -> Optional[int]:
        """
        Retrieves the data stored under the given key as an integer.

        Args:
            key (str): The key of the data to be retrieved.

        Returns:
            Optional[int]: The retrieved data as an integer,
            or None if the key does not exist.
        """
        return self.get(key, lambda x: int(x.decode()))

    def replay(self, method: Callable) -> None:
        """
        Displays the history of calls for a particular method.

        Args:
            method (Callable): The method/function whose
            history of calls to display.
        """
        # Prepare Redis keys for inputs and outputs
        key_inputs = method.__qualname__ + ":inputs"
        key_outputs = method.__qualname__ + ":outputs"

        # Fetch inputs and outputs lists from Redis
        inputs = self._redis.lrange(key_inputs, 0, -1)
        outputs = self._redis.lrange(key_outputs, 0, -1)

        # Print header with method name and number of calls
        print(f"{method.__qualname__} was called {len(inputs)} times:")

        # Iterate over inputs and outputs using zip
        for inp, out in zip(inputs, outputs):
            # Decode input (stored as bytes)
            input_str = inp.decode()

            # Print formatted output
            print(f"{method.__qualname__}(*{input_str}) -> {out.decode()}")
