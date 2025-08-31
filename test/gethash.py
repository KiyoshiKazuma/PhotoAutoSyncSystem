
import os
import hashlib

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

# 使用例
if __name__ == "__main__":
    # ハッシュ値を計算したいフォルダのパスを設定してください
    target_folder = 'C:\\Users\\makiy\\programing\\python\\PhotoAutoSyncSystem\\test\\dir'  # 例

    if not os.path.isdir(target_folder):
        print(f"エラー: 指定されたパス '{target_folder}' はフォルダではありません。")
    else:
        print(f"フォルダ '{target_folder}' 内のファイルのハッシュ値を計算しています...\n")
        
        # os.walk()でフォルダ内を再帰的に探索
        for root, dirs, files in os.walk(target_folder):
            for file_name in files:
                file_path = os.path.join(root, file_name)
                file_hash = get_file_hash(file_path)
                
                if file_hash:
                    # ファイル名とハッシュ値を出力
                    print(f"ファイル: {file_name}")
                    print(f"パス: {file_path}")
                    print(f"SHA-256ハッシュ: {file_hash}\n")