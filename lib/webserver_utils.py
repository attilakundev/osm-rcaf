import re


def split_messages_between_newlines(array_of_strings):
    for index, string in enumerate(array_of_strings):
        array_of_strings[index] = string.split('\n')
        array_of_strings[index] = find_link_in_the_line(array_of_strings[index])
        array_of_strings[index] = [[index_of_array_of_strings, line] for index_of_array_of_strings, line in
                                   enumerate(array_of_strings[index])]

    return array_of_strings


def find_link_in_the_line(lines_in_a_string):
    for index, line in enumerate(lines_in_a_string):
        words = line.split(' ')
        for word_index, word in enumerate(words):
            if "https://" in word:
                words[word_index] = '<a href="' + word + '">' + word + "</a>"
        # rebuild words back into the lines of the string
        rebuilt_string = ""
        for word in words:
            rebuilt_string += word + " "
        lines_in_a_string[index] = rebuilt_string
    return lines_in_a_string