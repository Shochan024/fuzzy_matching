import os
from invoke import task
from src.transporter.fetch_data import PieceTitleFetcher

@task
def fetch(c, data_path='sample.tsv'):
  # 格納先フォルダがなければ再帰的に作成
  path     = '/'.join(['data', data_path])
  dir_name = os.path.dirname(path)
  if not os.path.exists(dir_name):
    os.makedirs(dir_name)

  # データを取得
  print('Fetching piece titles..')
  fetcher = PieceTitleFetcher(data_path=path)
  fetcher.fetch(limit=10)
  print(f"The data was exported to the {path} directory.")


def prepair(c, input_data_path, output_data_path):
  pass
