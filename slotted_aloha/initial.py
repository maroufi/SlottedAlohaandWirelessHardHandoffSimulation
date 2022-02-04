from enum import Enum
import random
import os
import time


class StationStatus(Enum):
    NewRequest = 1
    BackloggedRequest = 2


class Station:
    def __init__(self, status):
        self.__status = status
        self.__is_sender = False

    def send(self):
        self.__is_sender = True

    def do_not_send(self):
        self.__is_sender = False

    def is_sender(self):
        return self.__is_sender

    def get_status(self):
        return self.__status

    def make_new_request(self):
        self.__status = StationStatus.NewRequest

    def make_backlogged_request(self):
        self.__status = StationStatus.BackloggedRequest


if __name__ == '__main__':
    max_tp_new_request_sending_probability = 0
    max_tp_backlogged_request_sending_probability = 0
    min_tp_new_request_sending_probability = 0
    min_tp_backlogged_request_sending_probability = 0
    maximum_throughput = 0
    minimum_throughput = float("inf")
    stations = []
    number_of_stations = 10
    for i in range(number_of_stations):
        stations.append(Station(StationStatus.NewRequest))

    for i in range(4000, 5000, 10):
        maximum_throughput = 0
        minimum_throughput = float("inf")
        new_request_sending_probability = i / (number_of_stations * 1000)
        for j in range(4000, 5000, 10):
            backlogged_request_sending_probability = j / (number_of_stations * 1000)
            all_spend_slot_count = 0
            used_slot_count = 0
            for k in range(0, 10000):
                sender_count = 0
                for station in stations:
                    a = random.randrange(0, 1000000)
                    if station.get_status() == StationStatus.NewRequest and a / 1000000 < new_request_sending_probability:
                        station.send()
                        sender_count += 1

                    elif station.get_status() == StationStatus.BackloggedRequest and \
                            a / 1000000 < backlogged_request_sending_probability:
                        station.send()
                        sender_count += 1

                all_spend_slot_count += 1
                if sender_count == 1:
                    used_slot_count += 1

                for station in stations:
                    if station.is_sender():
                        station.do_not_send()
                        if sender_count == 1:
                            station.make_new_request()
                        if sender_count > 1:
                            station.make_backlogged_request()

            throughput = used_slot_count * 100 / all_spend_slot_count
            if throughput > maximum_throughput:
                maximum_throughput = throughput
                max_tp_backlogged_request_sending_probability = backlogged_request_sending_probability
                max_tp_new_request_sending_probability = new_request_sending_probability

            if throughput < minimum_throughput:
                minimum_throughput = throughput
                min_tp_backlogged_request_sending_probability = backlogged_request_sending_probability
                min_tp_new_request_sending_probability = new_request_sending_probability

        print("a: %f b: %f throughput: %f"
              % (max_tp_new_request_sending_probability, max_tp_backlogged_request_sending_probability,
                 maximum_throughput))

        print("a: %f b: %f throughput: %f"
              % (min_tp_new_request_sending_probability, min_tp_backlogged_request_sending_probability,
                 minimum_throughput))
