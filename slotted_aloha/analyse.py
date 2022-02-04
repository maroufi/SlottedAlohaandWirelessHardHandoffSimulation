from math import factorial
import numpy

rounding_amount = 30


def combine(n, m):
    result = factorial(n) / factorial(m) / factorial(n - m)
    return result


# Probability that have i new request when there are n backlogged
def i_new_request_prop(i, n, m, a):
    if i > m - n:
        return 0
    result = combine(m - n, i) * (a ** i) * ((1 - a) ** (m - n - i))
    return result


# Probability that have i backlogged request when there are n backlogged
def i_backlogged_request_prop(i, n, b):
    if i > n:
        return 0
    result = combine(n, i) * (b ** i) * ((1 - b) ** (n - i))
    return result


def set_transition_matrix_index(row_index, column_index, m, a, b):
    state = row_index
    step = column_index - row_index

    if 2 <= step <= m - state:
        result = i_new_request_prop(step, state, m, a)
        return round(result, rounding_amount)
    elif step == 1:
        result = i_new_request_prop(1, state, m, a) * \
                 (1 - i_backlogged_request_prop(0, state, b))
        return round(result, rounding_amount)
    elif step == 0:
        result = i_new_request_prop(1, state, m, a) * (i_backlogged_request_prop(0, state, b)) + \
                 i_new_request_prop(0, state, m, a) * (1 - i_backlogged_request_prop(1, state, b))
        return round(result, rounding_amount)
    elif step == -1:
        result = i_new_request_prop(0, state, m, a) * \
                 (i_backlogged_request_prop(1, state, b))
        return round(result, rounding_amount)

    return 0


if __name__ == '__main__':
    number_of_stations = 10
    b = [0] * number_of_stations
    b.append(1)
    max_throughput = 0
    max_tp_new_request_sending_probability = 0
    max_tp_backlogged_request_sending_probability = 0
    min_throughput = float("inf")
    min_tp_new_request_sending_probability = 0
    min_tp_backlogged_request_sending_probability = 0
    for g in range(100, number_of_stations * 1000, 100):
        for h in range(g + 100, number_of_stations * 1000, 100):
            transition_matrix = []
            reward = []
            new_request_sending_probability = g / (number_of_stations * 1000)
            backlogged_request_sending_probability = h / (number_of_stations * 1000)

            for k in range(0, number_of_stations + 1):
                row = []
                for j in range(0, number_of_stations):
                    element = set_transition_matrix_index(k, j, number_of_stations, new_request_sending_probability,
                                                          backlogged_request_sending_probability)

                    if element < 0:
                        print(element)
                    if k == j:
                        element -= 1
                    row.append(element)

                row.append(1)
                transition_matrix.append(row)

                r = i_new_request_prop(1, k, number_of_stations, new_request_sending_probability) * \
                    (i_backlogged_request_prop(0, k, backlogged_request_sending_probability)) + \
                    i_new_request_prop(0, k, number_of_stations, new_request_sending_probability) * \
                    (i_backlogged_request_prop(1, k, backlogged_request_sending_probability))
                r = round(r, rounding_amount)
                reward.append(r)

            v = numpy.matmul(b, numpy.linalg.inv(transition_matrix))
            throughput = 0
            for k in range(number_of_stations + 1):
                if v[k] < 0:
                    print(v[k])
                throughput += v[k] * reward[k]

            if throughput > max_throughput:
                max_throughput = throughput
                max_tp_new_request_sending_probability = new_request_sending_probability
                max_tp_backlogged_request_sending_probability = backlogged_request_sending_probability

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
