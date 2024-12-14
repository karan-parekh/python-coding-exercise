import os
import logging
from coding_exercise.domain.model.cable import Cable

# Usually I use dotenv but since it's just one file, os.getenv is sufficient.
DEBUG = os.getenv("DEBUG", "False")

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
        self.padding = None

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
        pieces = times + 1 

        logging.debug(f"Cable of length {length}. Split {times} times. Results in {pieces} pieces")

        if not self.longest_int:
            self.longest_int = length // pieces

        logging.debug(f"Longest integer length {self.longest_int}")
        
        if self.longest_int == 1:
            # if the longest int is 1, then the cable will be divided in the same number of pieces as the length of the cable
            return self.cables_of_len_1(length, name)
        
        remaining_len = length - (self.longest_int * times)
                       
        if not self.cable_count:
            self.cable_count = pieces+1 if remaining_len > self.longest_int else pieces

        self.padding = len(str(self.cable_count))

        logging.debug(f"Appending {times} cables of len {self.longest_int} to the result array")
        self.append_to_result(self.longest_int, name, times)

        if remaining_len > self.longest_int:
            logging.debug(f"Remaining len {remaining_len} > longest int {self.longest_int}")
            remaining_times = remaining_len // self.longest_int
            logging.debug(f"Split it again {remaining_times} times")
            self.split(Cable(remaining_len, name), remaining_times)

        elif remaining_len:
            logging.debug(f"Remaining len {remaining_len} <= longest int {self.longest_int}")
            logging.debug(f"Appending 1 cable of remaining len {remaining_len} to the result array")
            self.append_to_result(remaining_len, name, times=1)

        logging.debug(f"Total cables in array: {len(self.result)}")
        return self.result

    def append_to_result(self, length, name, times):
        for _ in range(times):
            tail = f"{self.last_count}".zfill(self.padding)
            self.result.append(Cable(length, f"{name}-{tail}"))
            self.last_count += 1
    
    def cables_of_len_1(self, length, name):
        padding = len(str(length))
        result = []
        for c in range(length):
            tail = f"{c}".zfill(padding)
            result.append(Cable(1, f"{name}-{tail}"))

        return result