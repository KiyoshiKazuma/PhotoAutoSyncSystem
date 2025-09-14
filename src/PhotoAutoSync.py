import os
import threading
import time
import hashlib
from datetime import datetime
import shutil

# シンボル定義
EQUAL = 0
CHANGE = 1
NOT_FOUND = 2

ADD = 1
REMOVE = 2
CHANGE = 3

# ユースケース定義
USECASE_Non = 0
USECASE_Add = 1
USECASE_Del = 2
USECASE_Edi = 3
USECASE_DelDel = 4
USECASE_DelEdi = 5
USECASE_EdiEdi = 6

# 同期処理定義
SYNC_None = 0
SYNC_A = 1
SYNC_D = 2
SYNC_E = 3
SYNC_AA = 4
SYNC_DD = 5
SYNC_EE = 6

# デバッグモード
DEBUG_LEVEL = 0

def get_file_hash(file_path, hash_algorithm='sha256'):
    """
    指定されたファイルのハッシュ値を計算する関数
    :param file_path: ハッシュ値を計算するファイルのパス
    :param hash_algorithm: 使用するハッシュアルゴリズム（例: 'md5', 'sha1', 'sha256'）
    :return: ハッシュ値の文字列、またはエラーの場合はNone
    """
    try:
        # 指定されたハッシュアルゴリズムのオブジェクトを作成
        hash_obj = hashlib.new(hash_algorithm)
        
        # ファイルをバイナリモードで開き、チャンクごとに読み込む
        with open(file_path, 'rb') as f:
            while chunk := f.read(8192):  # チャンクサイズは適宜調整可能
                hash_obj.update(chunk)
                
        return hash_obj.hexdigest()
        
    except FileNotFoundError:
        print(f"エラー: ファイル '{file_path}' が見つかりません。")
        return None
    except Exception as e:
        print(f"エラー: {e}")
        return None

# ファイル情報
class file_info:
    # プロパティの宣言
    path: str # ファイルの相対パス
    hash: str # ファイルのハッシュ値
    
    def __init__(self, path: str, hash: str):
        self.path = path
        self.hash = hash

def count_files(root_dir):
    file_count = 0
    for _, _, files in os.walk(root_dir):
        file_count += len(files)
    return file_count

class composition_info:
    # プロパティの宣言
    files: list[file_info]

    def __init__(self):
        self.files = []
                
    def add_file(self, file: file_info):
        self.files.append(file)
        
    def delete_file(self, file: file_info):
        # filesリストから指定されたfile_infoオブジェクトを削除
        self.files.remove(file)
        
    def clear(self):
        self.files = []

    # ファイル情報を読み込む
    def read(self, input_file: str):
        if DEBUG_LEVEL >= 2:
            print(f"DEBUG:COMPOSITION_INFO: Reading composition info from {input_file}")
        # ファイルが存在するか確認
        if os.path.isfile(input_file):
            with open(input_file, "r") as f:
                for line in f:
                    # 行からファイルパスとハッシュを抽出
                    if line.startswith("File:"): 
                        line_split = line.split(", Hash:")
                        file_path = line_split[0].replace("File: ", "").strip()
                        file_hash = line_split[1].strip()
                        file = file_info(file_path, file_hash)
                        self.add_file(file)
    
    # ファイル情報を書き込む
    def write(self, output_file: str):
        if DEBUG_LEVEL >= 1:
            print(f"DEBUG:COMPOSITION_INFO: Writing composition info to {output_file}")
        with open(output_file, "w") as f:
            for file in self.files:
                f.write(f"File: {file.path}, Hash: {file.hash}\n")

    def print_files(self):
        for file in self.files:
            print(f"File: {file.path}, Hash: {file.hash}")

    def compare(self, otherfile: file_info):
        # ファイルの存在とハッシュ値の一致を確認
        if DEBUG_LEVEL >= 2:
            print(f"DEBUG: COMPOSITION_INFO: Comparing with {otherfile.path}")
        for file in self.files:
            if file.path == otherfile.path:
                if file.hash == otherfile.hash:
                    if DEBUG_LEVEL >= 2:
                        print(f"DEBUG: COMPOSITION_INFO: the same file {file.path} in {otherfile.path} is found.")
                    return EQUAL
                else:
                    if DEBUG_LEVEL >= 2:
                        print(f"DEBUG: COMPOSITION_INFO: the different file {file.path} in {otherfile.path} is found.")
                    return CHANGE
        if DEBUG_LEVEL >= 2:
            print(f"DEBUG: COMPOSITION_INFO: the file {otherfile.path} is not found.")
        return NOT_FOUND


# 構成情報の差分
class composition_diff_info:
    # プロパティの宣言
    added_files: list[file_info]
    removed_files: list[file_info]
    changed_files: list[file_info]

    def __init__(self):
        self.added_files = []
        self.removed_files = []
        self.changed_files = []
    
    # 構成情報の差分を取得
    def compare(self, compositon_base: composition_info, compositon_new: composition_info):
        # 2つの構成情報を比較し、差分を取得する
        for file in compositon_base.files:
            result = compositon_new.compare(file)
            if result == EQUAL:
                continue
            elif result == CHANGE:
                self.append_changed_file(file)
            elif result == NOT_FOUND:
                self.append_removed_file(file)
        for file in compositon_new.files:
            result = compositon_base.compare(file)
            if result == EQUAL:
                continue
            elif result == CHANGE:
                continue
            elif result == NOT_FOUND:
                self.append_added_file(file)
                
    # 指定のファイル情報が差分情報に含まれているか確認
    def diff_type(self, file: file_info) -> int:
        if file.path in [f.path for f in self.added_files]:
            return ADD
        elif file.path in [f.path for f in self.removed_files]:
            return REMOVE
        elif file.path in [f.path for f in self.changed_files]:
            return CHANGE
        return EQUAL

    def append_added_file(self, file: file_info):
        self.added_files.append(file)

    def append_removed_file(self, file: file_info):
        self.removed_files.append(file)

    def append_changed_file(self, file: file_info):
        self.changed_files.append(file)
    
    def remove_diff_file(self, file: file_info):
        if file in self.added_files:
            self.added_files.remove(file)
        elif file in self.removed_files:
            self.removed_files.remove(file)
        elif file in self.changed_files:
            self.changed_files.remove(file)

    def print(self):
        print("Added files:")
        for file in self.added_files:
            print(f"  {file.path}")

        print("Removed files:")
        for file in self.removed_files:
            print(f"  {file.path}")

        print("Changed files:")
        for file in self.changed_files:
            print(f"  {file.path}")

    # 差分情報をファイルに書き込む
    def write(self, output_file: str):
        with open(output_file, "w") as f:
            for file in self.added_files:
                f.write(f"Added: {file.path}\n")
            for file in self.removed_files:
                f.write(f"Removed: {file.path}\n")
            for file in self.changed_files:
                f.write(f"Changed: {file.path}\n")
    
    # 差分情報をファイルから読み込む
    def read(self, input_file: str):
        # ファイルが存在するか確認
        if os.path.isfile(input_file):            
            with open(input_file, "r") as f:
                for line in f:
                    if line.startswith("Added:"):
                        file_path = line.replace("Added:", "").strip()
                        file = file_info(file_path, "")
                        self.append_added_file(file)
                    elif line.startswith("Removed:"):
                        file_path = line.replace("Removed:", "").strip()
                        file = file_info(file_path, "")
                        self.append_removed_file(file)
                    elif line.startswith("Changed:"):
                        file_path = line.replace("Changed:", "").strip()
                        file = file_info(file_path, "")
                        self.append_changed_file(file)

# リポジトリ情報
class repository_info:
    # プロパティの宣言
    repository_root_path: str # ディレクトリのルートパス
    composition_file_path: str # 構成情報データのパス
    history_file_path: str # 差分情報のパス
    composition: composition_info # ディレクトリ内の構成情報
    composition_history: composition_diff_info # 構成情報の差分履歴

    def __init__(self, repository_root_path: str, composition_file_path: str , history_file_path: str):
        # パスがディレクトリであることを確認
        if not os.path.isdir(repository_root_path):
            raise NotADirectoryError(f"{repository_root_path} is not a valid directory")

        # プロパティの初期化
        
        self.repository_root_path = repository_root_path
        
        self.composition = composition_info()
        self.composition_file_path = composition_file_path

        self.composition_history = composition_diff_info()
        self.history_file_path = history_file_path

    # リポジトリ内のファイルを走査し、構成情報を取得
    def get_repository_info(self):
        cnt = 0
        cnt_total = count_files(self.repository_root_path)
        
        time_start = time.time()

        # ディレクトリ内のファイル情報を更新
        self.composition.clear()
        
        for root, dirs, files in os.walk(self.repository_root_path):
            for filename in files:
                 # 絶対パスを取得
                absolute_file_path = os.path.join(root, filename)

                # ルートディレクトリ(self.repository_root_path)からの相対パスを取得
                relative_file_path = os.path.relpath(absolute_file_path, self.repository_root_path)

                file_path = relative_file_path
                file_hash = get_file_hash(absolute_file_path)
                self.composition.add_file(file_info(file_path, file_hash))
                
                # 進捗を表示
                cnt += 1
                if(cnt%1000 == 0):
                    time_cur = time.time()
                    progress_rate = (cnt / cnt_total) * 100
                    progress_time = time_cur - time_start
                    remaining_time = (progress_time / progress_rate) * (100 - progress_rate)
                    print(f"updating {self.repository_root_path} : {cnt} / {cnt_total} files  (progress: {progress_rate:.2f}%, remaining: {remaining_time:.2f} seconds)")
    
    # 構成情報の差分を確認し、更新する
    def update_diff(self):
        
        # 既存の差分情報を読み込む
        self.read_diff()
        
        # 変更前の構成情報を読み込む
        composition_pre = composition_info()
        composition_pre.read(self.composition_file_path)

        # 構成情報の差分を取得し、更新
        self.composition_history.compare(composition_pre, self.composition)
        
        if DEBUG_LEVEL >= 1:
            print(f"DEBUG: REPOSITORY_INFO: Repository {self.repository_root_path} diff updated.")
            print("DEBUG: REPOSITORY_INFO: Current diff:")
            self.composition_history.print()
        
        # 差分情報をファイルに書き込む
        self.write_diff()

    # 構成情報をファイルに書き込む
    def write_repository_info(self):
        self.composition.write(self.composition_file_path)

    # 構成情報をファイルから読み込む
    def read_repository_info(self):
        self.composition.read(self.composition_file_path)

    
    # 差分情報をファイルに書き込む
    def write_diff(self):
        self.composition_history.write(self.history_file_path)

    # 差分情報をファイルから読み込む
    def read_diff(self):
        self.composition_history.read(self.history_file_path)
        
                
    # リポジトリ情報を更新
    def update(self):
        # リポジトリ内のファイルを走査し、構成情報を取得
        self.get_repository_info()
        
        # 構成情報の差分を確認し、更新する
        self.update_diff()
        
        # 構成情報をファイルに書き込む
        self.write_repository_info()
        
        if DEBUG_LEVEL >= 2:
            print(f"DEBUG: REPOSITORY_INFO: Repository {self.repository_root_path} updated.")
            print(f"DEBUG: REPOSITORY_INFO: Composition info written to {self.composition_file_path}")
            print(f"DEBUG: REPOSITORY_INFO: Diff info written to {self.history_file_path}")
            print("DEBUG: REPOSITORY_INFO: Current composition:")
            self.composition.print_files()
            print("DEBUG: REPOSITORY_INFO: Current diff:")
            self.composition_history.print()




class management_info:
    # プロパティの宣言
    config_file_path: str                    # 設定ファイルのパス
    repository1: repository_info             # リポジトリ1の情報
    repository2: repository_info             # リポジトリ2の情報
    repository1_root_path: str               # リポジトリ1のルートパス
    repository2_root_path: str               # リポジトリ2のルートパス
    repository1_repository_info_path: str    # リポジトリ1のファイルデータパス
    repository2_repository_info_path: str    # リポジトリ2のファイルデータパス
    repository1_history_path: str            # リポジトリ1の履歴データパス
    repository2_history_path: str            # リポジトリ2の履歴データパス
    composition_diff: composition_diff_info  # 構成情報の差分
    back_up_folder_path: str                 # バックアップフォルダのパス
    log_file_path: str                       # ログファイルのパス

    def __init__(self,config_file_path: str):
        self.config_file_path = config_file_path
        self.readconfig()
        self.repository1 = repository_info(
            self.repository1_root_path,
            self.repository1_repository_info_path,
            self.repository1_history_path
        )
        self.repository2 = repository_info(
            self.repository2_root_path,
            self.repository2_repository_info_path,
            self.repository2_history_path
        )
        self.composition_diff = composition_diff_info()
        if(self.repository1 is None or self.repository2 is None):
            raise ValueError("Repository paths are not set correctly in the config file")

    def readconfig(self):
        with open(self.config_file_path, "r", encoding='utf-8') as f:
            lines = f.readlines()
            self.repository1_root_path = lines[1].strip().split(": ")[1]
            self.repository1_repository_info_path = lines[1].strip().split(": ")[2]
            self.repository1_history_path = lines[1].strip().split(": ")[3]
            self.repository2_root_path = lines[2].strip().split(": ")[1]
            self.repository2_repository_info_path = lines[2].strip().split(": ")[2]
            self.repository2_history_path = lines[2].strip().split(": ")[3]
            self.back_up_folder_path = lines[4].strip().split(": ")[1]
            self.log_file_path = lines[6].strip().split(": ")[1]
            
        if DEBUG_LEVEL >= 1:
            print(f"DEBUG: MANAGEMENT_INFO: Reading config from {self.config_file_path}")
            print(f"DEBUG: MANAGEMENT_INFO: Repository 1 root path: {self.repository1_root_path}")
            print(f"DEBUG: MANAGEMENT_INFO: Repository 1 composition file path: {self.repository1_repository_info_path}")
            print(f"DEBUG: MANAGEMENT_INFO: Repository 1 history path: {self.repository1_history_path}")
            print(f"DEBUG: MANAGEMENT_INFO: Repository 2 root path: {self.repository2_root_path}")
            print(f"DEBUG: MANAGEMENT_INFO: Repository 2 composition file path: {self.repository2_repository_info_path}")
            print(f"DEBUG: MANAGEMENT_INFO: Repository 2 history path: {self.repository2_history_path}")
            print(f"DEBUG: MANAGEMENT_INFO: Backup folder path: {self.back_up_folder_path}")

    # 2つのリポジトリの情報を更新
    def update(self):
    #    t1 = threading.Thread(target=self.repository1.update)
    #    t2 = threading.Thread(target=self.repository2.update)
    #    t1.start()
    #    t2.start()
    #    t1.join()
    #    t2.join()
        if DEBUG_LEVEL >= 1:
            print("DEBUG: REPOSITORY_INFO: Updating repositories...")
        self.repository1.update()
        self.repository2.update()
    
    # 2つのリポジトリの構成情報を比較する
    def compare_repositories(self):
        
        self.composition_diff.compare(self.repository1.composition, self.repository2.composition)
        if DEBUG_LEVEL >= 1:
            print("DEBUG: COMPOSITION_DIFF: Comparing repositories...")
            self.composition_diff.print()
        
    # 2つのリポジトリの構成情報の差分をマージする
    def merge_diffs(self):
        # 1 リポジトリ間の差分情報をマージ
        # 1-1 リポジトリ1のみに存在するファイルをマージ
        for file in self.composition_diff.added_files:
            # リポジトリ1,2の変更履歴に対象のファイル情報がない場合(変更履歴の取得漏れ or 初期差分)
            # リポジトリ1にファイルをコピーする。
            if (file.path not in [f.path for f in self.repository1.composition_history.added_files] and
                file.path not in [f.path for f in self.repository1.composition_history.removed_files] and
                file.path not in [f.path for f in self.repository1.composition_history.changed_files] and
                file.path not in [f.path for f in self.repository2.composition_history.added_files] and
                file.path not in [f.path for f in self.repository2.composition_history.removed_files] and
                file.path not in [f.path for f in self.repository2.composition_history.changed_files]):
                self.copy_file_repository2_to_1(file)
        # 1-2 リポジトリ2のみに存在するファイルをマージ
        for file in self.composition_diff.removed_files:
            # リポジトリ1,2の変更履歴に対象のファイル情報がない場合(変更履歴の取得漏れ or 初期差分)
            # リポジトリ2にファイルをコピーする。
            if (file.path not in [f.path for f in self.repository1.composition_history.added_files] and
                file.path not in [f.path for f in self.repository1.composition_history.removed_files] and
                file.path not in [f.path for f in self.repository1.composition_history.changed_files] and
                file.path not in [f.path for f in self.repository2.composition_history.added_files] and
                file.path not in [f.path for f in self.repository2.composition_history.removed_files] and
                file.path not in [f.path for f in self.repository2.composition_history.changed_files]):
                self.copy_file_repository1_to_2(file)

        # 1-3 リポジトリ1とリポジトリ2で差分があるファイル
        for file in self.composition_diff.changed_files:
            # リポジトリ1,2の変更履歴に対象のファイル情報がない場合
            # コンフリクト
            print(f"Conflict: File {file.path} changed in both repositories.")
        
        # 2 リポジトリ1の更新情報をマージ
        # 2-1 追加されたファイルをマージ
        for file in self.repository1.composition_history.added_files:
            # 対象ファイルの差分情報を取得
            diff_type = self.composition_diff.diff_type(file)
        
            if diff_type == EQUAL:
                # 差分がない場合、マージは不要のため更新情報を削除する
                self.repository1.composition_history.remove_diff_file(file)
            elif diff_type == ADD:
                # リポジトリ1に追加されたファイルが、リポジトリ2のみに存在する場合
                # ありえないユースケースのためエラーログを出力。更新情報は保持する
                print(f"Error: File {file.path} exists only in repository1. This should not happen.")
            elif diff_type == REMOVE:
                # リポジトリ1に追加されたファイルが、リポジトリ1のみに存在する場合
                # リポジトリ2にファイルをコピーする。
                self.copy_file_repository1_to_2(file)
                # 更新情報を削除する
                self.repository1.composition_history.remove_diff_file(file)
            elif diff_type == CHANGE:
                # リポジトリ1に追加されたファイルが、リポジトリ2のファイルと差分がある場合
                # コンフリクト(リポジトリ1とリポジトリ2の両方で変更)
                print(f"Conflict: File {file.path} changed in both repositories.")

        # 2-2 削除されたファイルをマージ
        for file in self.repository1.composition_history.removed_files:
            # 対象ファイルの差分情報を取得
            diff_type = self.composition_diff.diff_type(file)
        
            if diff_type == EQUAL:
                # 差分がない場合、マージは不要のため更新情報を削除する
                self.repository1.composition_history.remove_diff_file(file)
            elif diff_type == ADD:
                # リポジトリ1に削除されたファイルが、リポジトリ2のみに存在する場合
                # リポジトリ2からファイルを削除する。
                self.move_file_repository2_to_backup(file)
                # 更新情報を削除する
                self.repository1.composition_history.remove_diff_file(file)
            elif diff_type == REMOVE:
                # リポジトリ1に削除されたファイルが、リポジトリ1のみに存在する場合
                # ありえないユースケースのためエラーログを出力。更新情報は保持する
                print(f"Error: File {file.path} deleted only in repository1. This should not happen.")
            elif diff_type == CHANGE:
                # リポジトリ1に削除されたファイルが、リポジトリ2のファイルと差分がある場合
                # コンフリクト(リポジトリ1で削除、リポジトリ2で変更)
                print(f"Conflict: File {file.path} deleted in repository1 and changed in repository2.")                
                
        # 2-3 変更されたファイルをマージ
        for file in self.repository1.composition_history.changed_files:
            # 対象ファイルの差分情報を取得
            diff_type = self.composition_diff.diff_type(file)
        
            if diff_type == EQUAL:
                # 差分がない場合、マージは不要のため更新情報を削除する
                self.repository1.composition_history.remove_diff_file(file)
            elif diff_type == CHANGE:
                # リポジトリ1に変更されたファイルが、リポジトリ2と差分がある場合
                # リポジトリ2の更新履歴により分岐
                repository2_diff_type = self.repository2.composition_history.diff_type(file)
                if repository2_diff_type == EQUAL:
                    # リポジトリ2の更新履歴がない場合、リポジトリ1のファイルをリポジトリ2にコピーする
                    self.copy_file_repository1_to_2(file)
                    # 更新情報を削除する
                    self.repository1.composition_history.remove_diff_file(file)
                elif repository2_diff_type == CHANGE:
                    # リポジトリ2の更新履歴も変更の場合、コンフリクト(リポジトリ1とリポジトリ2の両方で変更)
                    # 暫定的にマージを実行せず、シリアルログに出力する
                    print(f"Conflict: File {file.path} changed in both repositories.")
                elif repository2_diff_type == ADD:
                    # リポジトリ2の更新履歴が追加の場合、コンフリクト(リポジトリ1とリポジトリ2の両方で変更)
                    # 暫定的にマージを実行せず、シリアルログに出力する
                    print(f"Conflict: File {file.path} changed in repository1 and added in repository2.")
                elif repository2_diff_type == REMOVE:
                    # リポジトリ2の更新履歴が削除の場合、コンフリクト(リポジトリ1で変更、リポジトリ2で削除)
                    # 暫定的にマージを実行せず、シリアルログに出力する
                    print(f"Conflict: File {file.path} changed in repository1 and removed in repository2.")                
            elif diff_type == ADD:
                # リポジトリ1に変更されたファイルが、リポジトリ2のみに存在する場合
                # ありえないユースケースのためエラーログを出力。更新情報は保持する
                print(f"Error: File {file.path} changed only in repository1. This should not happen.")
            elif diff_type == REMOVE:
                # リポジトリ1に変更されたファイルが、リポジトリ1のみに存在する場合
                # リポジトリ2にファイルをコピーする。
                self.copy_file_repository1_to_2(file)
                # 更新情報を削除する
                self.repository1.composition_history.remove_diff_file(file)
        
        # 3 リポジトリ2の更新情報をマージ
        # 3-1 追加されたファイルをマージ
        for file in self.repository2.composition_history.added_files:
            # 対象ファイルの差分情報を取得
            diff_type = self.composition_diff.diff_type(file)
        
            if diff_type == EQUAL:
                # 差分がない場合、マージは不要のため更新情報を削除する
                self.repository2.composition_history.remove_diff_file(file)
            elif diff_type == ADD:
                # リポジトリ2に追加されたファイルが、リポジトリ2のみに存在する場合
                # リポジトリ1にファイルをコピーする。
                self.copy_file_repository2_to_1(file)
                # 更新情報を削除する
                self.repository2.composition_history.remove_diff_file(file)
            elif diff_type == REMOVE:
                # リポジトリ2に追加されたファイルが、リポジトリ1のみに存在する場合
                # ありえないユースケースのためエラーログを出力。更新情報は保持する
                print(f"Error: File {file.path} exists only in repository2. This should not happen.")                
            elif diff_type == CHANGE:
                # リポジトリ2に追加されたファイルが、リポジトリ1のファイルと差分がある場合
                # コンフリクト(リポジトリ1とリポジトリ2の両方で変更)
                print(f"Conflict: File {file.path} changed in both repositories.")

        # 3-2 削除されたファイルをマージ
        for file in self.repository2.composition_history.removed_files:
            # 対象ファイルの差分情報を取得
            diff_type = self.composition_diff.diff_type(file)
        
            if diff_type == EQUAL:
                # 差分がない場合、マージは不要のため更新情報を削除する
                self.repository2.composition_history.remove_diff_file(file)
            elif diff_type == ADD:
                # リポジトリ2に削除されたファイルが、リポジトリ2のみに存在する場合
                # ありえないユースケースのためエラーログを出力。更新情報は保持する
                print(f"Error: File {file.path} deleted only in repository2. This should not happen.")
            elif diff_type == REMOVE:
                # リポジトリ2に削除されたファイルが、リポジトリ1のみに存在する場合
                # リポジトリ1からファイルを削除する。
                self.move_file_repository1_to_backup(file)
                # 更新情報を削除する
                self.repository2.composition_history.remove_diff_file(file)
            elif diff_type == CHANGE:
                # リポジトリ2に削除されたファイルが、リポジトリ1のファイルと差分がある場合
                # コンフリクト(リポジトリ1で変更、リポジトリ2で削除)
                print(f"Conflict: File {file.path} deleted in repository1 and changed in repository2.")

        # 3-3 変更されたファイルをマージ
        for file in self.repository2.composition_history.changed_files:
            # 対象ファイルの差分情報を取得
            diff_type = self.composition_diff.diff_type(file)
        
            if diff_type == EQUAL:
                # 差分がない場合、マージは不要のため更新情報を削除する
                self.repository2.composition_history.remove_diff_file(file)
            elif diff_type == CHANGE:
                # リポジトリ2に変更されたファイルが、リポジトリ1と差分がある場合
                # リポジトリ1の更新履歴により分岐
                repository1_diff_type = self.repository1.composition_history.diff_type(file)
                if repository1_diff_type == EQUAL:
                    # リポジトリ1の更新履歴がない場合、リポジトリ2のファイルをリポジトリ1にコピーする
                    self.copy_file_repository2_to_1(file)
                    # 更新情報を削除する
                    self.repository1.composition_history.remove_diff_file(file)
                elif repository1_diff_type == CHANGE:
                    # リポジトリ1の更新履歴も変更の場合、コンフリクト(リポジトリ1とリポジトリ2の両方で変更)
                    # 暫定的にマージを実行せず、シリアルログに出力する
                    print(f"Conflict: File {file.path} changed in both repositories.")
                elif repository1_diff_type == ADD:
                    # リポジトリ1の更新履歴が追加の場合、コンフリクト(リポジトリ1とリポジトリ2の両方で変更)
                    # 暫定的にマージを実行せず、シリアルログに出力する
                    print(f"Conflict: File {file.path} changed in repository1 and added in repository2.")
                elif repository1_diff_type == REMOVE:
                    # リポジトリ1の更新履歴が削除の場合、コンフリクト(リポジトリ1で削除、リポジトリ2で変更)
                    # 暫定的にマージを実行せず、シリアルログに出力する
                    print(f"Conflict: File {file.path} changed in repository1 and removed in repository2.")                
            elif diff_type == ADD:
                # リポジトリ2に変更されたファイルが、リポジトリ2のみに存在する場合
                # リポジトリ1にファイルをコピーする。
                self.copy_file_repository2_to_1(file)
                # 更新情報を削除する
                self.repository2.composition_history.remove_diff_file(file)
            elif diff_type == REMOVE:
                # リポジトリ2に変更されたファイルが、リポジトリ1のみに存在する場合
                # ありえないユースケースのためエラーログを出力。更新情報は保持する
                print(f"Error: File {file.path} changed only in repository2. This should not happen.")
                


    # 2つのリポジトリの情報と更新情報をファイルに書き込む
    def write(self):
        self.repository1.write_repository_info()
        self.repository1.write_diff()
        self.repository2.write_repository_info()
        self.repository2.write_diff()
        
    def copy_file(self, src: str, dst: str, file: file_info):
        src_path = os.path.join(src, file.path)
        dst_path = os.path.join(dst, file.path)
        #　コピー先にファイルが存在する場合、上書きされるため、事前にバックアップを取得する
        if os.path.exists(dst_path):
            if src == self.repository1.repository_root_path:
                self.move_file_repository2_to_backup(file)
            else:
                self.move_file_repository1_to_backup(file)
        dst_dir = os.path.dirname(dst_path)
        if not os.path.exists(dst_dir):
            os.makedirs(dst_dir)
        print(f"Copying {src_path} to {dst_path}")
        #ログファイルにコピー情報を出力
        with open(self.log_file_path, "a", encoding='utf-8') as log_file:
            log_file.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Copying {src_path} to {dst_path}\n")
        shutil.copy2(src_path, dst_path)
    
    def move_file(self, src: str, file: file_info):
        src_path = os.path.join(src, file.path)
        # バックアップ先のファイル名はタイムスタンプを付与する
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        dst_path = os.path.join(self.back_up_folder_path, f"{timestamp}_{file.path}")
        dst_dir = os.path.dirname(dst_path)
        if not os.path.exists(dst_dir):
            os.makedirs(dst_dir)
        print(f"Moving {src_path} to {dst_path}")
        #ログファイルに移動情報を出力
        with open(self.log_file_path, "a", encoding='utf-8') as log_file:
            log_file.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Moving {src_path} to {dst_path}\n")
        shutil.move(src_path, dst_path)

    def copy_file_repository1_to_2(self, file: file_info):
        self.copy_file(self.repository1.repository_root_path, self.repository2.repository_root_path, file)
        
    def copy_file_repository2_to_1(self, file: file_info):
        self.copy_file(self.repository2.repository_root_path, self.repository1.repository_root_path, file)
    
    def move_file_repository1_to_backup(self, file: file_info):
        self.move_file(self.repository1.repository_root_path, file)
        
    def move_file_repository2_to_backup(self, file: file_info):
        self.move_file(self.repository2.repository_root_path, file)


if __name__ == "__main__":
    config_file_path = ".\\config"
    management = management_info(config_file_path)
    print("Start updating repositories...")
    management.update()
    print("Comparing repositories...")
    management.compare_repositories()
    print("Merging diffs...")
    management.merge_diffs()
    print("Update ")
    management.update()
    print("Writing results...")
    management.write()