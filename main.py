"""
visionPigeon - internship task
Author: Filip Bali
Python version: 3.10.2
"""

import os
import json
from datetime import datetime

DATA_DIR = "data/"


def datetime_converter(date):
    if len(date) == 32:  # longer datatime variant
        return datetime.strptime(date, "%Y-%m-%dT%H:%M:%S.%f%z")
    else:  # shorter datatime variant
        return datetime.strptime(date, "%Y-%m-%dT%H:%M:%S%z")


def get_median(arr):
    arr.sort()
    arr_len = len(arr)

    if arr_len % 2 == 0:
        first_middle_idx = int(arr_len / 2)
        second_middle_idx = first_middle_idx + 1
        return (arr[first_middle_idx] + arr[second_middle_idx]) / 2
    else:
        middle_idx = int(arr_len / 2) + 1
        return arr[middle_idx]


def print_results():
    print('Number of unique users: {}'.format(len(unique_users)))
    print('Number of unique requests: {}'.format(len(unique_items)))
    print('Average time between item_id requests: {}'.format(sum(request_diff_arr) / len(request_diff_arr)))
    print('Median time between item_id requests: {}'.format(get_median(request_diff_arr)))
    print('Maximum number of requests per a single item_id for which the variant '
          'similarInJsonList: {}'.format(similarInJsonList_counter))


if __name__ == '__main__':

    unique_users = set()
    unique_items = set()
    request_diff_arr = []
    similarInJsonList_counter = 0

    # Iterate over all files in DATA_DIR
    for filename in os.scandir(DATA_DIR):
        f = open(filename.path)
        json_data = json.load(f)  # Load data as JSON

        # Iterate over all users
        for user_id, user_values in json_data.items():
            user_values.pop('variant')  # not important -> delete

            # Save user_id
            unique_users.add(user_id)

            # Iterate over user_values
            # Get items
            for item_id in user_values:
                # Save unique requests
                # Multiple requests of the same item count as one
                # Also it is not important if multiple users request same item
                unique_items.add(item_id)

                # Delete empty arrays
                item_values = [arr for arr in user_values[item_id] if arr]

                # If multiple requests
                if len(user_values) > 1:

                    # Save first visit datatime
                    previous_visit_datetime = datetime_converter(item_values[0][0][0])
                    temp_similarInJsonList_counter = 0

                    # If first visit returned variant as similarInJsonList
                    if item_values[0][0][1] == 'similarInJsonList':
                        temp_similarInJsonList_counter += 1

                    # Iterate over remaining items
                    for request_details in item_values[0][1:]:

                        # If returned variant as similarInJsonList
                        if request_details[1] == 'similarInJsonList':
                            temp_similarInJsonList_counter += 1

                        visit_datetime = datetime_converter(request_details[0])

                        time_diff = (visit_datetime - previous_visit_datetime).total_seconds()
                        if time_diff:
                            request_diff_arr.append(time_diff)

                        previous_visit_datetime = visit_datetime

                    # Save maximum number of requests per a single item_id
                    # for which the variant similarInJsonList was returned.
                    if temp_similarInJsonList_counter > similarInJsonList_counter:
                        similarInJsonList_counter = temp_similarInJsonList_counter

    print_results()
