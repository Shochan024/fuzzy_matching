import os
import csv
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

class PieceTitleFetcher:
  HEADERS = ['piece_title']

  def __init__(self, data_path):
    self.data_path = data_path
    self.client    = spotipy.Spotify(
        client_credentials_manager = SpotifyClientCredentials(
          client_id     = os.environ['SPOTYFI_CLIENT_ID'],
          client_secret = os.environ['SPOTYFI_CLIENT_SECRET']
      )
    )

  def fetch(self, limit=1000, verbose=False):
    tracks = self.__get_tracks(limit, verbose)

    # 結果をtsvに出力
    with open(self.data_path, 'w', newline='', encoding='utf-8') as tsvfile:
      writer = csv.writer(tsvfile, delimiter='\t')
      writer.writerow(self.HEADERS)
      for track in tracks: writer.writerow([track])


  def __get_tracks(self, limit, verbose=False, tracks=None, offset=0):
    # 初期実行時に返り値を初期化
    if tracks is None: tracks = []

    # track数が上限に達したら処理停止
    if len(tracks) >= limit: return tracks

    # アルバムから作品タイトルを取得
    results = self.client.new_releases(limit=50, offset=offset)
    for album in results['albums']['items']:
      album_tracks = self.client.album_tracks(album['id'])['items']

      for track in album_tracks:
        piece_name = track['name'].replace('\t', ' ')
        tracks.append(piece_name)

        if verbose: print(f"{len(tracks)}作品目: {piece_name}")
        if len(tracks) >= limit: return tracks

    return self.__get_tracks(limit, verbose, tracks, offset + 50)
