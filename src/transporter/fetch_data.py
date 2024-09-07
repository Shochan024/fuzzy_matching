import os
import csv
import time
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

class PieceTitleFetcher:
  MAX_RETRIES    = 10
  YEAR_INCREMENT = 10
  HEADERS        = ['piece_title']

  def __init__(self, data_path):
    self.data_path = data_path
    self.client    = spotipy.Spotify(
        client_credentials_manager = SpotifyClientCredentials(
          client_id     = os.environ['SPOTYFI_CLIENT_ID'],
          client_secret = os.environ['SPOTYFI_CLIENT_SECRET']
      )
    )

  def fetch(self, limit=1000, verbose=False):
    tracks     = []
    start_year = 1960
    end_year   = start_year + self.YEAR_INCREMENT - 1
    while start_year <= 2024 and len(tracks) < limit:
      for genre in ['rock', 'pop', 'jazz', 'classical']:
        tracks += self.__get_tracks(start_year, end_year, genre, limit - len(tracks), verbose)

      start_year += self.YEAR_INCREMENT
      end_year   += self.YEAR_INCREMENT - 1

    # 結果をtsvに出力
    with open(self.data_path, 'w', newline='', encoding='utf-8') as tsvfile:
      writer = csv.writer(tsvfile, delimiter='\t')
      writer.writerow(self.HEADERS)
      for track in tracks: writer.writerow([track])


  def __get_tracks(self, start_year, end_year, genre, limit, verbose=False, tracks=None, offset=0, retries=0):
    # 初期実行時に返り値を初期化
    if tracks is None: tracks = []

    # track数が上限に達したら処理停止
    if len(tracks) >= limit: return tracks

    # アルバムから作品タイトルを取得
    try:
      # 1つのqueryに対しoffsetの上限が1,000までであるため年代を区切って取得する
      query   = f'year:{start_year}-{end_year} genre:{genre}'
      results = self.client.search(q=query, type='track', limit=50, offset=offset)
    except spotipy.exceptions.SpotifyException as e:
      if e.http_status == 429:
        # APIリクエスト上限に引っかかった際は、Retry-Afterを取得してその時間待機
        retry_after = int(e.headers.get('Retry-After', 1))
        print(f"Rate limit exceeded. Retrying after {retry_after} seconds.")
        time.sleep(retry_after)

        if retries >= self.MAX_RETRIES:
          print("Max retries reached. Stopping...")
          return tracks

        return self.__get_tracks(start_year, end_year, genre, limit, verbose, tracks, offset, retries + 1) # 再試行
      else:
        print(f"An error occurred: {e}")
        return tracks


    for track in results['tracks']['items']:
      piece_name = track['name'].replace('\t', ' ')
      tracks.append(piece_name)

      if verbose: print(f"残り{limit - len(tracks)}作品目: {piece_name}")

      if len(tracks) >= limit:
        return tracks

    return self.__get_tracks(start_year, end_year, genre, limit, verbose, tracks, offset + 50)
