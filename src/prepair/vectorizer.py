import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer

class TfIdf:
  def __init__(self, input_data_path):
    self.input_data_path = input_data_path
    self.vectorizer      = TfidfVectorizer()

  def exec(self, header, output_data_path, delimiter='\t'):
    # テキストデータを取得
    df        = pd.read_csv(self.input_data_path, sep=delimiter)
    text_data = df[header].dropna()
    
    return self.vectorizer.fit_transform(text_data)

  def get_feature_names_out(self):
    return self.vectorizer.get_feature_names_out()
