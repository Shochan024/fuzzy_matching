import os
import pandas as pd
import scipy.sparse as sparse
from invoke import task
from src.transporter.fetch_data import PieceTitleFetcher
from src.prepair.vectorizer import TfIdf

@task
def fetch(c, output_data_path='sample.tsv', limit=100):
  # 格納先フォルダがなければ再帰的に作成
  path     = '/'.join(['data', output_data_path])
  dir_name = os.path.dirname(path)
  if not os.path.exists(dir_name):
    os.makedirs(dir_name)

  # データを取得
  print('Fetching piece titles..')
  fetcher = PieceTitleFetcher(data_path=path)
  fetcher.fetch(limit=limit)
  print(f"The data was exported to the {path} directory.")


@task
def prepair(c, header, input_data_path, output_data_path, delimiter='\t'):
  # 格納先フォルダがなければ再帰的に作成
  expanded_output_data_path = '/'.join(['data', output_data_path])
  expanded_input_data_path  = '/'.join(['data', input_data_path])
  dir_name                  = os.path.dirname(expanded_output_data_path)
  if not os.path.exists(dir_name):
    os.makedirs(dir_name)

  print('Now vectorizing...')
  # 行列のキャッシュファイルのpathを作成
  sparse_matrix_cache_path = '.'.join([os.path.splitext(expanded_output_data_path)[0], 'npz'])

  # ベクトル化
  vectorize    = TfIdf(input_data_path=expanded_input_data_path)
  tfidf_matrix = vectorize.exec(header=header, output_data_path=expanded_output_data_path, delimiter=delimiter)

  # 出力
  sparse.save_npz(sparse_matrix_cache_path, tfidf_matrix)
  vocab = vectorize.get_feature_names_out()
  pd.DataFrame(vocab).to_csv(expanded_output_data_path, sep=delimiter, index=False, header=False)

  print(f"The data was exported to the {sparse_matrix_cache_path} directory.")
