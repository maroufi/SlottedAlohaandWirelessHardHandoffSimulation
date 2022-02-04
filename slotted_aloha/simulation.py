from enum import Enum
import random


class StationStatus(Enum):
    NewRequest = 1
    BackloggedRequest = 2
    Sending = 3


if __name__ == '__main__':
    max_throughput = 0
    max_tp_new_request_sending_probability = 0
    max_tp_backlogged_request_sending_probability = 0
    min_throughput = float("inf")
    min_tp_new_request_sending_probability = 0
    min_tp_backlogged_request_sending_probability = 0
    stations = []
    number_of_stations = 10
    for i in range(number_of_stations):
        stations.append(StationStatus.NewRequest)

    for i in range(100, number_of_stations * 1000, 100):
        new_request_sending_probability = i / (number_of_stations * 1000)
        for j in range(i + 100, number_of_stations * 1000, 100):
            backlogged_request_sending_probability = j / (number_of_stations * 1000)
            all_spend_slot_count = 0
            used_slot_count = 0
            for k in range(0, 1000):
                sender_count = 0
                for station in stations:
                    a = random.randrange(0, number_of_stations * 10)
                    if station == StationStatus.NewRequest and \
                            a / (number_of_stations * 10) < new_request_sending_probability:
                        station = StationStatus.Sending
                        sender_count += 1

                    elif station == StationStatus.BackloggedRequest and \
                            a / (number_of_stations * 10) < backlogged_request_sending_probability:
                        station = StationStatus.Sending
                        sender_count += 1

                all_spend_slot_count += 1
                if sender_count == 1:
                    used_slot_count += 1

                for station in stations:
                    if station == StationStatus.Sending:
                        if sender_count == 1:
                            station = StationStatus.NewRequest
                        if sender_count > 1:
                            station = StationStatus.BackloggedRequest

            throughput = used_slot_count * 100 / all_spend_slot_count
            if throughput > max_throughput:
                max_throughput = throughput
                max_tp_backlogged_request_sending_probability = backlogged_request_sending_probability
                max_tp_new_request_sending_probability = new_request_sending_probability

            if throughput < min_throughput:
                min_throughput = throughput
                min_tp_new_request_sending_probability = new_request_sending_probability
                min_tp_backlogged_request_sending_probability = backlogged_request_sending_probability

    print("max_throughput: %f related new request sending probability: %f "
          "related backlogged request sending probability: %f "
          % (max_throughput, max_tp_new_request_sending_probability, max_tp_backlogged_request_sending_probability))

    print("min_throughput: %f related new request sending probability: %f "
          "related backlogged request sending probability: %f "
          % (min_throughput, min_tp_new_request_sending_probability, min_tp_backlogged_request_sending_probability))
