import os
from invoke import task
from src.transporter.fetch_data import PieceTitleFetcher

@task
def prepair(c, data_path='sample.tsv'):
  path     = '/'.join(['data', data_path])
  dir_name = os.path.dirname(path)
  if not os.path.exists(dir_name):
    os.makedirs(dir_name)

  print('Fetching piece titles..')
  fetcher = PieceTitleFetcher(data_path=path)
  fetcher.fetch(limit=10)
  print(f"The data was exported to the {path} directory.")
