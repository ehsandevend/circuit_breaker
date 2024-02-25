from typing import int
from django.conf import settings
import time

class CircuitBreaker:
    def __init__(self) -> None:
        self.max_threshold = getattr(settings, "CIRCUIT_BREAKER_THRESHOLD", 3)
        self.reset_timeout: int = getattr(settings, "CIRCUIT_BREAKER_RESET_TIME", 50)
        self.debug: bool = getattr(settings, "CIRCUIT_BREAKER_DEBUG", False)
        self.failures: int = 0
        self.last_failure_time:int = 0
        self.is_circuit_open:bool = False

    def set_max_thresholds(self, times: int) -> None:
        self.max_threshold = times

    def set_reset_timeout(self, miliseconds: int) -> None:
        self.reset_timeout = miliseconds

    def execute(self) -> bool:
        if self.is_open() and time.time() - self.last_failure_time < self.reset_timeout:
            if self.debug:
                print(f"Circuit breaker is open. {time.time() - self.last_failure_time} < {self.reset_timeout}")
            return False
        return True

    def handle_failure(self) -> None:
        self.failures += 1
        if self.failures >= self.max_threshold:
            self.open_circuit()

    def open_circuit(self) -> None:
        self.is_circuit_open = True
        self.last_failure_time = time.time()
        if self.debug:
            print("Circuit is open. Will not execute function until reset timeout.")

    def is_open(self) -> bool:
        return self.is_circuit_open

    def reset(self) -> None:
        self.failures = 0
        self.is_circuit_open = False
        if self.debug:
            print("circuit breaker is closed")