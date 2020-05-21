import re

def remove_URL(text):
    '''
    去除网络链接
    :param text:
    :return:
    '''
    url = re.compile(r'https?://\S+|www\.\S+')
    return url.sub(r'',text)

# example="New competition launched :https://www.kaggle.com/c/nlp-getting-started"
# # #
# # # print(remove_URL(example))