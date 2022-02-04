import numpy
import bisect
import matplotlib.pyplot as plt


def generate_exponential_random_variable(ratio):
    return numpy.random.exponential(1/ratio)


if __name__ == '__main__':
    simulation_time = 120

    number_of_channel = 1000
    new_call_ratio = 300
    hand_off_call_ratio = 280
    completion_time_ratio = 1 / 3
    departure_time_ratio = 1 / 4
    min_of_guard_channel = 1
    max_of_guard_channel = 5

    guard_channels = []
    blocking_probabilities = []
    dropping_probabilities = []
    for number_of_guard_channels in range(1,max_of_guard_channel+1):
        number_of_busy_channel = 0
        new_call_arrival_times = []
        new_call_completion_times = []
        new_call_departure_times = []
        total_time = 0
        while total_time < simulation_time:
            next_call = generate_exponential_random_variable(new_call_ratio)
            new_call_arrival_times.append(next_call)
            total_time += next_call
            new_call_completion_times.append(generate_exponential_random_variable(completion_time_ratio))
            new_call_departure_times.append(generate_exponential_random_variable(departure_time_ratio))

        hand_off_call_arrival_times = []
        hand_off_call_completion_times = []
        hand_off_call_departure_times = []
        total_time = 0
        while total_time < simulation_time:
            next_call = generate_exponential_random_variable(hand_off_call_ratio)
            hand_off_call_arrival_times.append(next_call)
            total_time += next_call
            hand_off_call_completion_times.append(generate_exponential_random_variable(completion_time_ratio))
            hand_off_call_departure_times.append(generate_exponential_random_variable(departure_time_ratio))

        total_time = 0
        number_of_new_calls = len(new_call_arrival_times)
        number_of_hand_off_call = len(hand_off_call_arrival_times)
        number_of_dropped_call = 0
        number_of_blocked_call = 0
        ending_time_of_calls = []
        while total_time < simulation_time:
            if number_of_busy_channel == 0:
                first_event = min(new_call_arrival_times[0], hand_off_call_arrival_times[0])
                if new_call_arrival_times[0] == first_event:
                    total_time += new_call_arrival_times[0]
                    bisect.insort(ending_time_of_calls,
                                  min(new_call_completion_times[0], new_call_departure_times[0]))
                    number_of_busy_channel += 1
                    hand_off_call_arrival_times[0] -= new_call_arrival_times[0]

                    new_call_arrival_times.pop(0)
                    new_call_completion_times.pop(0)
                    new_call_departure_times.pop(0)
                else:
                    total_time += hand_off_call_arrival_times[0]
                    bisect.insort(ending_time_of_calls,
                                  min(hand_off_call_completion_times[0], hand_off_call_departure_times[0]))
                    number_of_busy_channel += 1
                    new_call_arrival_times[0] -= hand_off_call_arrival_times[0]

                    hand_off_call_arrival_times.pop(0)
                    hand_off_call_completion_times.pop(0)
                    hand_off_call_departure_times.pop(0)

            elif number_of_busy_channel < number_of_channel - number_of_guard_channels:
                first_event = min(new_call_arrival_times[0], hand_off_call_arrival_times[0], ending_time_of_calls[0])
                if new_call_arrival_times[0] == first_event:
                    total_time += new_call_arrival_times[0]
                    ending_time_of_calls = [element - new_call_arrival_times[0] for element in ending_time_of_calls]
                    bisect.insort(ending_time_of_calls,
                                  min(new_call_completion_times[0], new_call_departure_times[0]))
                    number_of_busy_channel += 1
                    hand_off_call_arrival_times[0] -= new_call_arrival_times[0]

                    new_call_arrival_times.pop(0)
                    new_call_completion_times.pop(0)
                    new_call_departure_times.pop(0)

                elif hand_off_call_arrival_times[0] == first_event:
                    total_time += hand_off_call_arrival_times[0]
                    ending_time_of_calls = [element - hand_off_call_arrival_times[0] for element in ending_time_of_calls]
                    bisect.insort(ending_time_of_calls,
                                  min(hand_off_call_completion_times[0], hand_off_call_departure_times[0]))
                    number_of_busy_channel += 1
                    new_call_arrival_times[0] -= hand_off_call_arrival_times[0]

                    hand_off_call_arrival_times.pop(0)
                    hand_off_call_completion_times.pop(0)
                    hand_off_call_departure_times.pop(0)

                elif ending_time_of_calls[0] == first_event:
                    total_time += ending_time_of_calls[0]
                    number_of_busy_channel -= 1
                    new_call_arrival_times[0] -= ending_time_of_calls[0]
                    hand_off_call_arrival_times[0] -= ending_time_of_calls[0]
                    ending_time_of_calls = [element - ending_time_of_calls[0] for element in ending_time_of_calls]
                    ending_time_of_calls.pop(0)

            elif number_of_channel - number_of_guard_channels <= number_of_busy_channel < number_of_channel:
                first_event = min(new_call_arrival_times[0], hand_off_call_arrival_times[0], ending_time_of_calls[0])

                if new_call_arrival_times[0] == first_event:
                    total_time += new_call_arrival_times[0]
                    ending_time_of_calls = [element - new_call_arrival_times[0] for element in ending_time_of_calls]
                    hand_off_call_arrival_times[0] -= new_call_arrival_times[0]
                    number_of_blocked_call += 1

                    new_call_arrival_times.pop(0)
                    new_call_completion_times.pop(0)
                    new_call_departure_times.pop(0)

                elif hand_off_call_arrival_times[0] == first_event:
                    total_time += hand_off_call_arrival_times[0]
                    ending_time_of_calls = [element - hand_off_call_arrival_times[0] for element in ending_time_of_calls]
                    bisect.insort(ending_time_of_calls,
                                  min(hand_off_call_completion_times[0], hand_off_call_departure_times[0]))
                    number_of_busy_channel += 1
                    new_call_arrival_times[0] -= hand_off_call_arrival_times[0]

                    hand_off_call_arrival_times.pop(0)
                    hand_off_call_completion_times.pop(0)
                    hand_off_call_departure_times.pop(0)

                elif ending_time_of_calls[0] == first_event:
                    total_time += ending_time_of_calls[0]
                    number_of_busy_channel -= 1
                    new_call_arrival_times[0] -= ending_time_of_calls[0]
                    hand_off_call_arrival_times[0] -= ending_time_of_calls[0]
                    ending_time_of_calls = [element - ending_time_of_calls[0] for element in ending_time_of_calls]
                    ending_time_of_calls.pop(0)

            elif number_of_busy_channel == number_of_channel:
                first_event = min(new_call_arrival_times[0], hand_off_call_arrival_times[0], ending_time_of_calls[0])

                if new_call_arrival_times[0] == first_event:
                    total_time += new_call_arrival_times[0]
                    ending_time_of_calls = [element - new_call_arrival_times[0] for element in ending_time_of_calls]
                    hand_off_call_arrival_times[0] -= new_call_arrival_times[0]
                    number_of_blocked_call += 1

                    new_call_arrival_times.pop(0)
                    new_call_completion_times.pop(0)
                    new_call_departure_times.pop(0)

                elif hand_off_call_arrival_times[0] == first_event:
                    total_time += hand_off_call_arrival_times[0]
                    ending_time_of_calls = [element - hand_off_call_arrival_times[0] for element in ending_time_of_calls]
                    new_call_arrival_times[0] -= hand_off_call_arrival_times[0]
                    number_of_dropped_call += 1

                    hand_off_call_arrival_times.pop(0)
                    hand_off_call_completion_times.pop(0)
                    hand_off_call_departure_times.pop(0)

                elif ending_time_of_calls[0] == first_event:
                    total_time += ending_time_of_calls[0]
                    number_of_busy_channel -= 1
                    new_call_arrival_times[0] -= ending_time_of_calls[0]
                    hand_off_call_arrival_times[0] -= ending_time_of_calls[0]
                    ending_time_of_calls = [element - new_call_arrival_times[0] for element in ending_time_of_calls]
                    ending_time_of_calls.pop(0)

        guard_channels.append(number_of_guard_channels)
        blocking_probability = number_of_blocked_call / number_of_new_calls
        blocking_probabilities.append(blocking_probability)
        print("blocking probability : %f" % blocking_probability)
        dropping_probability = number_of_dropped_call / number_of_hand_off_call
        dropping_probabilities.append(dropping_probability)
        print("dropping probability : %f" % dropping_probability)

    plt.plot(guard_channels, blocking_probabilities, label="Blocking Probability")

    plt.plot(guard_channels, dropping_probabilities, label="Dropping Probability")

    plt.xlabel('Number Of Guard Channels')
    plt.ylabel('Drop Or Blocking Probability')
    plt.title('Loss Probability Depend On Guard Channels')
    plt.legend()
    plt.show()
