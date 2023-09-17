from src.lib import webserver_utils


def test_split_messages_between_newlines():
    # Arrange
    messages_filled_with_line_breaks = ["This\nmessage\nhas\nline breaks.", "This\nhas some\ntoo.",
                                        "Here is a link:\nhttps://www.google.com"]
    # Act
    result = webserver_utils.split_messages_between_newlines(messages_filled_with_line_breaks)
    # Assert
    assert result[0] == [[0, "This "], [1, "message "], [2, "has "], [3, "line breaks. "]]
    assert result[1] == [[0, "This "], [1, "has some "], [2, "too. "]]
    assert result[2] == [[0, "Here is a link: "],
                         [1, "<a href=\"https://www.google.com\">https://www.google.com</a> "]]


def test_find_link_in_the_line():
    # Arrange
    list_without_url = ["This", "message",  "has", "line breaks."]
    list_with_url = ["Here is a link:", "https://www.google.com"]
    # Act
    result_no_link = webserver_utils.find_link_in_the_line(list_without_url)
    result_link = webserver_utils.find_link_in_the_line(list_with_url)
    # Assert
    assert result_no_link == ["This ", "message ",  "has ", "line breaks. "]
    assert result_link == ["Here is a link: ",
                           '<a href="https://www.google.com">https://www.google.com</a> ']
