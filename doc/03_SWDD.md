- [1.はじめに](#1はじめに)
- [2.管理機能(MNG)](#2管理機能mng)
  - [2.1.API(外部接続)](#21api外部接続)
    - [2.1.1.提供API一覧](#211提供api一覧)
    - [2.1.2.呼び出しAPI](#212呼び出しapi)
- [3. MANAGEMENT](#3-management)
- [4. REPOSITORY](#4-repository)
  - [4.1 概要](#41-概要)
    - [概要 : リポジトリ情報](#概要--リポジトリ情報)
    - [クラス名 : repository\_info](#クラス名--repository_info)
    - [インスタンス定義](#インスタンス定義)
  - [4.2 プロパティ](#42-プロパティ)
  - [4.3 メソッド](#43-メソッド)
    - [4.3.7 update](#437-update)
      - [概要](#概要)
      - [入力](#入力)
      - [出力](#出力)
      - [呼び出し関数](#呼び出し関数)
      - [詳細](#詳細)
    - [4.3.1 get\_repository\_info](#431-get_repository_info)
      - [概要](#概要-1)
      - [入力](#入力-1)
      - [出力](#出力-1)
      - [呼び出し関数](#呼び出し関数-1)
      - [詳細](#詳細-1)
    - [4.3.2 update\_diff](#432-update_diff)
      - [概要](#概要-2)
      - [入力](#入力-2)
      - [出力](#出力-2)
      - [呼び出し関数](#呼び出し関数-2)
      - [詳細](#詳細-2)
    - [4.3.3 write\_repository\_info](#433-write_repository_info)
      - [概要](#概要-3)
      - [入力](#入力-3)
      - [出力](#出力-3)
      - [呼び出し関数](#呼び出し関数-3)
      - [詳細](#詳細-3)
    - [4.3.4 read\_repository\_info](#434-read_repository_info)
      - [概要](#概要-4)
      - [入力](#入力-4)
      - [出力](#出力-4)
      - [呼び出し関数](#呼び出し関数-4)
      - [詳細](#詳細-4)
    - [4.3.5 write\_diff](#435-write_diff)
      - [概要](#概要-5)
      - [入力](#入力-5)
      - [出力](#出力-5)
      - [呼び出し関数](#呼び出し関数-5)
      - [詳細](#詳細-5)
    - [4.3.6 read\_diff](#436-read_diff)
      - [概要](#概要-6)
      - [入力](#入力-6)
      - [出力](#出力-6)
      - [呼び出し関数](#呼び出し関数-6)
      - [詳細](#詳細-6)
- [5. COMPOSITION](#5-composition)
- [6. COMPOSITION\_DIFF](#6-composition_diff)
- [7. MERGER](#7-merger)
- [8. FILEOPERATER](#8-fileoperater)
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

# 3. MANAGEMENT

# 4. REPOSITORY
## 4.1 概要
### 概要 : リポジトリ情報
### クラス名 : repository_info
### インスタンス定義
repository_info(repository_root_path, composition_file_path, history_file_path)


## 4.2 プロパティ

|プロパティ名|型|概要|
|:-|:-|:-|
|repository_root_path|str|ディレクトリのルートパス|
|composition_file_path|str|構成情報データのパス|
|history_file_path|str|変更履歴情報のパス|
|composition|composition_info|ディレクトリ内の構成情報|
|composition_history|composition_diff_info|構成情報の差分履歴|

## 4.3 メソッド

### 4.3.7 update
#### 概要 
リポジトリ情報を更新
#### 入力 
無し
#### 出力 
無し
#### 呼び出し関数
self.get_repository_info
self.update_diff
self.write_repository_info

#### 詳細
1. リポジトリ情報を取得
2. リポジトリの変更履歴を更新
3. 構成情報を書き出す

リポジトリを走査して、構成情報と変更履歴を取得し、ファイルを更新する。

### 4.3.1 get_repository_info
#### 概要 
走査してリポジトリ情報を取得する。
#### 入力 
self.repository_root_path
#### 出力 
self.composition
#### 呼び出し関数
count_files
composition.clear
get_file_hash
composition.add_file
#### 詳細
1. compositionをリセットする。
2. repository_root_path下のファイルを走査し、ファイル情報(ファイルの相対パスとハッシュ値)を取得する。
3. ファイル情報をcompositonに設定する。
1000ファイルごとに進捗を標準出力する。

### 4.3.2 update_diff
#### 概要 
構成情報の差分を確認し、更新する
#### 入力
self.repository_root_path
self.composition_file_path
self.composition

#### 出力
self.composition_history

#### 呼び出し関数
self.read_diff
composition.read
composition_diff.compare
self.write_diff

#### 詳細
1. history_file_pathのファイルから既存の変更履歴を読み出す。
2. composition_file_pathのファイルから前回の構成情報を読み出す。
3. 今回の構成情報と前回の構成情報を比較し、composition_historyを更新する。
4. composition_historyをファイルhistory_file_pathに書き出す。

### 4.3.3 write_repository_info
#### 概要 
構成情報をファイルに書き込む
#### 入力 
#### 出力 
#### 呼び出し関数
#### 詳細

### 4.3.4 read_repository_info
#### 概要 
構成情報をファイルから読み込む
#### 入力 
#### 出力 
#### 呼び出し関数
#### 詳細

### 4.3.5 write_diff
#### 概要 
差分情報をファイルに書き込む
#### 入力 
#### 出力 
#### 呼び出し関数
#### 詳細

### 4.3.6 read_diff
#### 概要 
差分情報をファイルから読み込む
#### 入力 
#### 出力 
#### 呼び出し関数
#### 詳細

# 5. COMPOSITION
# 6. COMPOSITION_DIFF
# 7. MERGER
# 8. FILEOPERATER


# 8.共通変数

|内容|変数名|値|
|:-|:-|:-|
|リポジトリ種別|
|サーバーリポジトリ|SERVER_REPOSITORY|1|
|クライアントリポジトリ|CLIENT_REPOSITORY|2|
|標準戻り値|
|正常|STD_OK|1|
|異常|STD_NG|0|
