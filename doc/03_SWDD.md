- [1.はじめに](#1はじめに)
- [2.管理機能(MNG)](#2管理機能mng)
  - [2.1.API(外部接続)](#21api外部接続)
    - [2.1.1.提供API一覧](#211提供api一覧)
    - [2.1.2.呼び出しAPI](#212呼び出しapi)
- [3.差分検出機能(DETECT)](#3差分検出機能detect)
- [4.同期処理機能(SYNC)](#4同期処理機能sync)
- [5.通知機能(NOTICE)](#5通知機能notice)
- [6.データ管理機能(DATA)](#6データ管理機能data)
- [7.コマンド操作機能(CMD)](#7コマンド操作機能cmd)
  - [7.1.ファイル複製機能](#71ファイル複製機能)
- [8.共通変数](#8共通変数)




# 1.はじめに

各コンポーネントに対して、一意に実装ができる粒度で設計を記載する。
下記コンポーネントの一覧
|機能名|略称|説明|
|:-|:-|:-|
|管理機能|MNG|各機能の呼び出し、結合を管理する機能|
|差分検出機能|DETECT|リポジトリの変化を検出する機能|
|同期処理機能|SYNC|リポジトリの同期処理を実行する機能|
|通知機能|NOTICE|コンフリクトの発生、リポジトリ容量に関する通知を実施し、レスポンスを受け取る機能|
|データ管理機能|DATA|リポジトリ構成やコンフリクトに関する情報を外部ファイルで管理する機能|
|コマンド操作機能|CMD|OSのシェルを操作しリポジトリ内のファイル操作を実行する機能|

# 2.管理機能(MNG)
## 2.1.API(外部接続)
### 2.1.1.提供API一覧
|要素|内容|
|:-|:-|
|機能概要|外部から同期処理開始要求を受け付けるAPI。APIを呼び出されたとき順次同期処理、通知処理を実施する。|
|関数名|mng_begin|
|引数|none|
|戻り値|none|
|備考|-|

### 2.1.2.呼び出しAPI
|要素|内容|
|:-|:-|
|機能概要|リポジトリの差分を検出する|
|関数名|detect_repository|
|引数|none|
|戻り値|none|
|備考|-|

|要素|内容|
|:-|:-|
|機能概要|構成情報の差分を検出する|
|関数名|detect_composition|
|引数|none|
|戻り値|none|
|備考|-|

|要素|内容|
|:-|:-|
|機能概要 |設定情報ファイルから設定情報を読み出す|
|関数名   |data_read_config|
|引数     |none|
|戻り値   |設定データ|
|備考     |-|



# 3.差分検出機能(DETECT)


# 4.同期処理機能(SYNC)
# 5.通知機能(NOTICE)
# 6.データ管理機能(DATA)
# 7.コマンド操作機能(CMD)
## 7.1.ファイル複製機能

|要素|内容||
|:-|:-|:-|
|機能概要|ファイルを複製する|
|関数名|cmd_file_copy|
|引数|src_repository|リポジトリ種別|
|^   |src_filepath|文字列|
|戻り値|std_ret|
|備考|-|

[src_repository]リポジトリの[src_filepath]のファイルを対リポジトリの[src_filepath]に複製する。
複製先に同じ名前のファイルがある場合は上書きする。
複製に失敗した場合は[STD_NG]を返す。
複製に成功した場合は[STD_OK]を返す。


# 8.共通変数

|内容|変数名|値|
|:-|:-|:-|
|リポジトリ種別|
|サーバーリポジトリ|SERVER_REPOSITORY|1|
|クライアントリポジトリ|CLIENT_REPOSITORY|2|
|標準戻り値|
|正常|STD_OK|1|
|異常|STD_NG|0|
