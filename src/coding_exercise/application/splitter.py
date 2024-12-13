import logging
from coding_exercise.domain.model.cable import Cable
import os

DEBUG = os.getenv("DEBUG", "False") # Usually I use dotenv but since it's just one file, os.getenv suffice.

logging.basicConfig(
    level=logging.DEBUG if DEBUG=="True" else logging.WARNING,
    format="{asctime}|{levelname}|{message}",
    style="{",
    datefmt="%H:%M",
)


class Splitter:

    def __init__(self):
        self.longest_int = None
        self.result = []
        self.cable_count = 0
        self.last_count = 0

    def __validate(self, cable: Cable, times: int):
        valid = True
        message = "Invalid inputs"
        length = cable.length

        if times >= length:
            valid = False
            message = f"Number of splits cannot be greater than or equal to the length of cable | {times} >= {length}"

        if length < 2 or cable.length > 1024:
            valid = False
            message = f"Length of cable must be between 2 and 1024 | length = {length}"

        if times < 1 or times > 64:
            valid = False
            message = f"Cannot split less than 1 times or more than 64 times | times = {times}"

        if not valid:
            raise ValueError(message)

    def split(self, cable: Cable, times: int) -> list[Cable]:
        self.__validate(cable, times)
        name = cable.name
        length = cable.length
        parts = times + 1

        logging.debug(f"For a cable of length {length}, split it {times} times. This means that there will be {parts} parts")

        if not self.longest_int:
            self.longest_int = length // parts

        logging.debug(f"Longest integer length is {self.longest_int}")
        
        if self.longest_int == 1:
            self.cable_count = length
            padding = len(str(self.cable_count))
            result = []
            for c in range(length):
                tail = f"{c}".zfill(padding)
                result.append(Cable(1, f"{name}-{tail}"))

            return result
        
        remaining_len = length - (self.longest_int * times)
                       
        if not self.cable_count:
            self.cable_count = parts+1 if remaining_len > self.longest_int else parts

        padding = len(str(self.cable_count))

        logging.debug(f"appending cable of len {self.longest_int} to the result array, {times} times")
        for c in range(times):
            tail = f"{self.last_count}".zfill(padding)
            self.result.append(Cable(self.longest_int, f"{name}-{tail}"))
            self.last_count += 1

        if remaining_len > self.longest_int:
            logging.debug(f"Since remaining len {remaining_len} > longest int {self.longest_int}")
            remaining_times = remaining_len // self.longest_int
            logging.debug(f"Split it again {remaining_times} times")
            self.split(Cable(remaining_len, name), remaining_times)
        elif remaining_len:
            logging.debug(f"Since remaining len {remaining_len} <= longest int {self.longest_int}")
            logging.debug(f"We append cable of remaining len {remaining_len} to the result array")
            tail = f"{self.last_count}".zfill(padding)
            self.result.append(Cable(remaining_len, f"{name}-{tail}"))
            self.last_count += 1

        logging.debug(f"Total cables in array: {len(self.result)}")
        return self.result