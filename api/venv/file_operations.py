import nltk
import shutil
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import os
import re 

nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('omw-1.4')


# root = "../data/cnn_dailymail/data/dailymail/stories/"
# root = "../data/cnn_dailymail/data/cnn/stories/"
# root = "../data/cnn_dailymail/data/subset/"

stop_words = set(stopwords.words('english'))
lemmatizer = WordNetLemmatizer()

def process_token(content):
    tokens = nltk.word_tokenize(content)
        
    result = []
    for word in tokens:
        # Lemmatize the tokens
        word = lemmatizer.lemmatize(word)
        
        # Remove punctuation and convert to lowercase
        word = re.sub(r'[^\w\s]', '', word).lower()
        if not word:
            continue

        # Remove stop words  
        if word not in stop_words:
            # Remove starting 0s
            if word.startswith("00"):
                word = word.lstrip('0')
            if word == "":
                continue

            result.append(word)
            
    return result

def read_file(file_path):
    with open(root+file_path, 'r') as file:
        
        content = file.read()
        content = content.split("@highlight")[0]
        
        # Tokenize the text
        result = process_token(content)

        return file_path, result
    
    
def get_all_files(folder_path):
    result = []
    for f in os.listdir(folder_path):
        if f.endswith("story"):
            result.append(f)
    return result


def copy_file(args):
    source, destination = args
    shutil.copyfile(source, destination)
    
    
if __name__ == '__main__':
    print(process_token("HeLLo W-orlD!"))