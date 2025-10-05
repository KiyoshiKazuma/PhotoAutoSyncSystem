import os
import sys

# ----------------------------------------------------
# 設定
# ----------------------------------------------------

# 処理対象のフォルダパスを指定してください
# 例: target_dir = "C:/Users/username/Documents/test_files"
# ここではスクリプトと同じディレクトリを指定しています
TARGET_DIR = "N:/Photos"

# 置き換え後の文字（非対応文字が見つかった場合に置き換えられる文字）
REPLACEMENT_CHAR = ""

# ----------------------------------------------------
# メイン処理
# ----------------------------------------------------

def is_encodable_to_cp932(text):
    """
    指定された文字列がCP932でエンコード可能かどうかをチェックする。
    エンコードに失敗する文字（非対応文字）がある場合はFalseを返す。
    """
    try:
        # 'strict'エラーハンドリングでエンコードを試みる
        text.encode('cp932', 'strict')
        return True
    except UnicodeEncodeError:
        return False

def clean_filename_for_cp932(filename, replacement):
    """
    ファイル名からCP932でエンコードできない文字を置き換え後の文字に置き換え、
    新しいファイル名を返す。
    """
    new_filename = []
    
    # 文字列を一文字ずつチェックし、非対応文字を置き換える
    for char in filename:
        if is_encodable_to_cp932(char):
            new_filename.append(char)
        else:
            new_filename.append(replacement)
            
    return "".join(new_filename)


def rename_files_in_directory(directory, replacement_char):
    """
    指定フォルダ内のすべてのファイルとフォルダ名をチェックし、
    CP932非対応文字を置き換えてリネームする（再帰的処理）。
    """
    
    # フォルダの存在確認
    if not os.path.isdir(directory):
        print(f"エラー: 指定されたディレクトリが見つかりません -> {directory}")
        return

    print(f"処理を開始します: {os.path.abspath(directory)}")
    
    # os.walk()でディレクトリを再帰的に走査
    for root, dirs, files in os.walk(directory, topdown=False):
        
        # 1. ファイルのリネーム
        for filename in files:
            old_path = os.path.join(root, filename)
            
            # クリーンアップ後のファイル名を取得
            new_filename = clean_filename_for_cp932(filename, replacement_char)
            
            # ファイル名が変更された場合のみリネームを実行
            if filename != new_filename:
                new_path = os.path.join(root, new_filename)
                
                try:
                    os.rename(old_path, new_path)
                    print(f"  [ファイル名変更] {filename} -> {new_filename}")
                except Exception as e:
                    print(f"  [エラー] ファイル {old_path} のリネームに失敗しました: {e}")

        # 2. サブフォルダのリネーム（ファイルより後に処理する必要がある）
        # フォルダ名を直接変更すると os.walk の `dirs` リストが壊れるため、
        # `dirs` の中身を更新することで対応する
        i = 0
        while i < len(dirs):
            dirname = dirs[i]
            old_path = os.path.join(root, dirname)
            
            # クリーンアップ後のフォルダ名を取得
            new_dirname = clean_filename_for_cp932(dirname, replacement_char)
            
            if dirname != new_dirname:
                new_path = os.path.join(root, new_dirname)
                
                try:
                    os.rename(old_path, new_path)
                    print(f"  [フォルダ名変更] {dirname} -> {new_dirname}")
                    
                    # リネームが成功した場合、`dirs` リスト内の元の名前を新しい名前に置き換える
                    # これにより os.walk の次のステップで新しい名前が正しく処理される
                    dirs[i] = new_dirname
                except Exception as e:
                    print(f"  [エラー] フォルダ {old_path} のリネームに失敗しました: {e}")
            
            i += 1

    print("\n✅ 処理が完了しました。")


if __name__ == "__main__":
    rename_files_in_directory(TARGET_DIR, REPLACEMENT_CHAR)