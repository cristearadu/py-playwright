
def get_names(data_list):
    return [x[0] for x in data_list]


def get_data(data_list):
    final_test_data = []

    # loop through all items from the list of test data
    for tuple_item in data_list:
        # if in the tuple is only the test description and test data
        if len(tuple_item) == 2:
            # select only the test data as a dictionary value
            final_test_data.append(tuple_item[1])
        else:
            # slice from the list of tuples the first tuple item
            final_test_data.append(tuple_item[1:])
    return final_test_data

