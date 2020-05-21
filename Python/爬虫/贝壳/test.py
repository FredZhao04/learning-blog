import string

def remove_punct(text):
    """
    将一段文字中的标点字符删除
    :param text: sring
    :return: string
    """
    table = str.maketrans('', '', string.punctuation)
    return text.translate(table)

# example = "I am a #king"
# print(remove_punct(example))
