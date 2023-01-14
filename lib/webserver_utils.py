def split_messages_between_spaces(array_of_strings):
    for index,string in enumerate(array_of_strings):
        array_of_strings[index] = string.split(' ')
    return array_of_strings