import os
import threading
import time

import gethash
import getfilecnt

# シンボル定義
EQUAL = 0
CHANGE = 1
NOT_FOUND = 2

class file_info:
    # プロパティの宣言
    path: str # ファイルの相対パス
    hash: str # ファイルのハッシュ値
    
    def __init__(self, path: str, hash: str):
        self.path = path
        self.hash = hash

class composition_diff_info:
    # プロパティの宣言
    added_files: list[file_info]
    removed_files: list[file_info]
    changed_files: list[file_info]

    def __init__(self):
        self.added_files = []
        self.removed_files = []
        self.changed_files = []

    def append_added_file(self, file: file_info):
        self.added_files.append(file)

    def append_removed_file(self, file: file_info):
        self.removed_files.append(file)

    def append_changed_file(self, file: file_info):
        self.changed_files.append(file)
        
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

    def write(self, output_file: str):
        with open(output_file, "w") as f:
            for file in self.added_files:
                f.write(f"Added: {file.path}\n")
            for file in self.removed_files:
                f.write(f"Removed: {file.path}\n")
            for file in self.changed_files:
                f.write(f"Changed: {file.path}\n")

class composition_info:
    # プロパティの宣言
    files: list[file_info]

    def __init__(self):
        self.files = []
                
    def add_file(self, file: file_info):
        self.files.append(file)
        
    def clear(self):
        self.files = []

    def readcomposition(self, input_file: str):
        # ファイル情報を読み込む
        with open(input_file, "r") as f:
            for line in f:
                # 行からファイルパスとハッシュを抽出
                if line.startswith("File:"):
                    file_info = line.split(", Hash:")
                    file_path = file_info[0].replace("File: ", "").strip()
                    file_hash = file_info[1].strip()
                    self.add_file(file_info(file_path, file_hash))
    
    def print(self):
        for file in self.files:
            print(f"File: {file.path}, Hash: {file.hash}")

    def compare(self, otherfile: file_info):
        for file in self.files:
            if file.path == otherfile.path:
                if file.hash == otherfile.hash:
                    return EQUAL
                else:
                    return CHANGE
        return NOT_FOUND

class repository_info:
    # プロパティの宣言
    repository_root_path: str # ディレクトリのパス
    composition_file_path: str # ファイル情報データのパス
    diff_file_path: str # 差分ファイルのパス
    composition: composition_info # ディレクトリ内の構成情報

    def __init__(self, repository_root_path: str, composition_file_path: str , diff_file_path: str):
        # パスがディレクトリであることを確認
        if not os.path.isdir(repository_root_path):
            raise NotADirectoryError(f"{repository_root_path} is not a valid directory")

        # プロパティの初期化
        self.repository_root_path = repository_root_path
        self.composition = composition_info()
        self.composition_file_path = composition_file_path
        self.diff_file_path = diff_file_path

    def update(self):
        cnt = 0
        cnt_total = getfilecnt.count_files(self.repository_root_path)
        
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
                file_hash = gethash.get_file_hash(absolute_file_path)
                self.composition.add_file(file_info(file_path, file_hash))
                
                # 進捗を表示
                cnt += 1
                if(cnt%1000 == 0):
                    time_cur = time.time()
                    progress_rate = (cnt / cnt_total) * 100
                    progress_time = time_cur - time_start
                    remaining_time = (progress_time / progress_rate) * (100 - progress_rate)
                    print(f"updating {self.repository_root_path} : {cnt} / {cnt_total} files  (progress: {progress_rate:.2f}%, remaining: {remaining_time:.2f} seconds)")

    def write(self):
        # ディレクトリ内のファイル情報を出力
        with open(self.composition_file_path, "w") as f:
            for file in self.composition.files:
                f.write(f"File: {file.path}, Hash: {file.hash}\n")

    def readcompositiondata(self):
        self. .readcomposition(self.composition_file_path)

    def check_change(self):
        # 変更を確認
        composition_diff = composition_diff_info()

        # 変更前の構成情報を読み込む
        composition_info_data_pre = composition_info()
        composition_info_data_pre.readcomposition(self.composition_file_path)

        # 変更後の構成情報を更新
        composition_info_data_cur = self.composition

        # ファイルの存在とハッシュ値の一致を確認
        for file in composition_info_data_cur.files:
            result = composition_info_data_pre.compare(file)
            if result == EQUAL:
                continue
            elif result == CHANGE:
                composition_diff.append_changed_file(file)
            elif result == NOT_FOUND:
                composition_diff.append_added_file(file)
        for file in composition_info_data_pre.files:
            result = composition_info_data_cur.compare(file)
            if result == EQUAL:
                continue
            elif result == CHANGE:
                continue
            elif result == NOT_FOUND:
                composition_diff.append_removed_file(file)

        return composition_diff

class management_info:
    # プロパティの宣言
    config_file_path: str    
    repository1: repository_info
    repository2: repository_info
    repository1_diff: composition_diff_info
    repository2_diff: composition_diff_info
    repository1_root_path: str
    repository2_root_path: str
    repository1_files_data_path: str
    repository2_files_data_path: str
    repository1_diff_data_path: str
    repository2_diff_data_path: str

    def __init__(self,config_file_path: str):
        self.config_file_path = config_file_path
        self.readconfig()
        self.repository1 = repository_info(
            self.repository1_root_path,
            self.repository1_files_data_path,
            self.repository1_diff_data_path
        )
        self.repository2 = repository_info(
            self.repository2_root_path,
            self.repository2_files_data_path,
            self.repository2_diff_data_path
        )
        if(self.repository1 is None or self.repository2 is None):
            raise ValueError("Repository paths are not set correctly in the config file")

    def readconfig(self):
        with open(self.config_file_path, "r", encoding='utf-8') as f:
            lines = f.readlines()
            self.repository1_root_path = lines[1].strip().split(": ")[1]
            self.repository1_files_data_path = lines[1].strip().split(": ")[2]
            self.repository1_diff_data_path = lines[1].strip().split(": ")[3]
            self.repository2_root_path = lines[2].strip().split(": ")[1]
            self.repository2_files_data_path = lines[2].strip().split(": ")[2]
            self.repository2_diff_data_path = lines[2].strip().split(": ")[3]

    def writeconfig(self):
        with open(self.config_file_path, "w") as f:
            f.write(f"Repository 1: {self.repository1_root_path}, {self.repository1_files_data_path}, {self.repository1_diff_data_path}\n")
            f.write(f"Repository 2: {self.repository2_root_path}, {self.repository2_files_data_path}, {self.repository2_diff_data_path}\n")

    def update_all(self):
        t1 = threading.Thread(target=self.repository1.update)
        t2 = threading.Thread(target=self.repository2.update)
        t1.start()
        t2.start()
        t1.join()
        t2.join()

    def write_repository_info_all(self):
        self.repository1.write()
        self.repository2.write()


    def check_change(self):
        self.repository_diff1 = self.repository1.check_change()
        self.repository_diff2 = self.repository2.check_change()
    

    def compare_compositiondata(self):
        # 2つのリポジトリの構成情報を比較する
        
        repository1 = self.repository1
        repository2 = self.repository2

        data1 = repository1.composition
        data2 = repository2.composition

        # ファイルの存在とハッシュ値の一致を確認
        for file in data1.files:
            result = data2.compare(file)
            if result == EQUAL:
                continue
            elif result == CHANGE:
                print(f"File {file.path} has different hash")
            elif result == NOT_FOUND:
                print(f"File {file.path} is missing in {repository2.repository_root_path}")
        for file in data2.files:
            result = data1.compare(file)
            if result == EQUAL:
                continue
            elif result == CHANGE:
                continue
            elif result == NOT_FOUND:
                print(f"File {file.path} is missing in {repository1.repository_root_path}")



if __name__ == "__main__":
    config_file_path = "C:\\Users\\makiy\\programing\\python\\PhotoAutoSyncSystem\\test\\config"
    management = management_info(config_file_path)
    management.update_all()
    management.write_repository_info_all()
    management.check_change()
    management.compare_compositiondata()
    management.write_repository_info_all()