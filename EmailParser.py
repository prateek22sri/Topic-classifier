import email.parser
import re
from os import listdir
from os.path import isfile, join
import string


def visible(element):
    if element.parent.name in ['style', 'script', '[document]', 'head', 'title']:
        return False
    elif re.match('<!--.*-->', str(element.encode("UTF-8"))):
        return False
    return True


class Parser:
    prsr = None
    stops = None
    h = None
    printable = None
    stops = ['i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', 'your', 'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', 'her', 'hers', 'herself', 'it', 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves', 'what', 'which', 'who', 'whom', 'this', 'that', 'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into', 'through', 'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don', 'should', 'now', 'd', 'll', 'm', 'o', 're', 've', 'y', 'ain', 'aren', 'couldn', 'didn', 'doesn', 'hadn', 'hasn', 'haven', 'isn', 'ma', 'mightn', 'mustn', 'needn', 'shan', 'shouldn', 'wasn', 'weren', 'won', 'wouldn']
    def __init__(self):
        self.prsr = email.parser.Parser()
        self.printable = set(string.printable)

    def plain_handler(self, plain_text):
        plain_text = re.sub("[ ]+", " ", plain_text)
        return_words = []
        plain_text = re.sub('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', "",
                            plain_text)
        # print(plain_text)
        for word in re.split('\\|!|@|#|\$|%|\^|&|\*|\)|\[|\]|\(|_|\+|=|-|~|;|:|\?|\"|\'|\.| |\n|>|<|\t|/|,|\||\}|\{|`',
                             plain_text):
            word = word.lower()
            if word not in self.stops:
                word = re.sub("[ ]+", " ", word)
                if len(word) > 0 and len(word) < 15 and not word.isdigit():
                    return_words.append(word)
        return return_words

    def parse(self, folder_path):
        current_files = [f for f in listdir(folder_path) if isfile(join(folder_path, f))]
        email_texts = []
        results = []

        for email_file in current_files:
            with open(folder_path + email_file, 'r') as fp:
                results.append((self.prsr.parse(fp), email_file))
        while len(results) > 0:
            result, file = results.pop()
            ctype = result.get_content_type()
            current_message = ""
            if result.is_multipart():
                for parts in result.walk():
                    if not parts.is_multipart():
                        if "html" in parts.get_content_type() or "plain" in parts.get_content_type():
                            current_message = parts.get_payload()
                            email_texts.append(self.plain_handler(current_message))
            elif "plain" in ctype or "html" in ctype:
                text = result.get_payload()
                email_texts.append(self.plain_handler(text))
        return email_texts
