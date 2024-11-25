def list_group(input_list, group_size):
    """
    Convert a list into a list of lists with a specified group size.
    """
    return [input_list[i:i + group_size] for i in range(0, len(input_list), group_size)]