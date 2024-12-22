#外部モジュールインポート
import shutil
import os
import glob
import hashlib
from pathlib import Path
#ユーザーモジュールインポート
import common

class cmd:
    def __init__(self,server_repository_path,client_repository_path):
        self.server_repository_path = server_repository_path
        self.client_repository_path = client_repository_path

    #ファイル複製機能
    def file_copy(self,src_repository,src_filepath):
        ret = common.STD_ERR
        if src_repository == common.SERVER_REPOSITORY :
            try:
                shutil.copy2(self.server_repository_path + "/" + src_filepath ,self.client_repository_path + "/" + src_filepath )
                ret = common.STD_OK
            except:
                ret = common.STD_ERR
        elif src_repository == common.CLIENT_REPOSITORY :
            try:
                shutil.copy2(self.client_repository_path + "/" + src_filepath ,self.server_repository_path + "/" + src_filepath )
                ret = common.STD_OK
            except:
                ret = common.STD_ERR

        return  ret

    #ファイル削除機能
    def file_delete(self, tgt_repository, tgt_filepath):
        ret = common.STD_ERR
        if (tgt_repository == common.SERVER_REPOSITORY):
            try:
                os.remove(self.server_repository_path + "/" + tgt_filepath)
                ret = common.STD_OK
            except:
                ret = common.STD_ERR
        elif (tgt_repository == common.CLIENT_REPOSITORY):
            try:
                os.remove(self.client_repository_path + "/" + tgt_filepath)
                ret = common.STD_OK
            except:
                ret = common.STD_ERR
        
        return ret

    #フォルダ追加機能
    def folder_add(self, tgt_repository ,tgt_folder_path):
        ret = common.STD_ERR
        if (tgt_repository == common.SERVER_REPOSITORY):
            try:
                os.mkdir(self.server_repository_path + "/" + tgt_folder_path)
                ret = common.STD_OK
            except:
                ret = common.STD_ERR
        elif (tgt_repository == common.CLIENT_REPOSITORY):
            try:
                os.mkdir(self.client_repository_path + "/" + tgt_folder_path)
                ret = common.STD_OK
            except:
                ret = common.STD_ERR
        
        return ret       
        
    #フォルダ削除機能
    def folder_delete(self, tgt_repository ,tgt_folder_path):
        ret = common.STD_ERR
        if (tgt_repository == common.SERVER_REPOSITORY):
            try:
                os.mkdir(self.server_repository_path + "/" + tgt_folder_path)
                ret = common.STD_OK
            except:
                ret = common.STD_ERR
        elif (tgt_repository == common.CLIENT_REPOSITORY):
            try:
                os.mkdir(self.client_repository_path + "/" + tgt_folder_path)
                ret = common.STD_OK
            except:
                ret = common.STD_ERR
        
        return ret       
        
    #フォルダパス変更機能
    def folder_move(self, tgt_repository, src_folder_path, tgt_folder_path):        
        ret = common.STD_ERR
        if (tgt_repository == common.SERVER_REPOSITORY):
            try:
                shutil.move(self.server_repository_path + "/" + src_folder_path, \
                            self.server_repository_path + "/" + tgt_folder_path)
                ret = common.STD_OK
            except:
                ret = common.STD_ERR
        elif (tgt_repository == common.CLIENT_REPOSITORY):
            try:
                shutil.move(self.client_repository_path + "/" + src_folder_path, \
                            self.client_repository_path + "/" + tgt_folder_path)
                ret = common.STD_OK
            except:
                ret = common.STD_ERR
        
        return ret       
    
    #ファイル検索機能
    def file_find(self, tgt_repository, tgt_file_path):
        ret = common.STD_ERR
        if (tgt_repository == common.SERVER_REPOSITORY):
            try:
                file = glob.glob(self.server_repository_path + "/" + tgt_file_path)
                if file == []:
                    ret = common.STD_NG
                else :
                    ret = common.STD_OK
            except:
                ret = common.STD_ERR
        elif (tgt_repository == common.CLIENT_REPOSITORY):
            try:
                file = glob.glob(self.client_repository_path + "/" + tgt_file_path)
                if file == []:
                    ret = common.STD_NG
                else :
                    ret = common.STD_OK
            except:
                ret = common.STD_ERR
        
        return ret       

    #ファイルハッシュ値取得機能
    def file_hash(self, tgt_repository, tgt_file_path):
        hash_value = ""
        if (tgt_repository == common.SERVER_REPOSITORY):
            try:
                path_tmp = self.server_repository_path + "\\" + tgt_file_path
                filedata = open(path_tmp,"rb").read()
                hash_value =hashlib.sha256(filedata).hexdigest()
            except:
                hash_value = ""
        elif (tgt_repository == common.CLIENT_REPOSITORY):
            try:
                filedata = open(self.client_repository_path + "/" + tgt_file_path,"rb").read()
                hash_value = str(hashlib.sha256(filedata).hexdigest())
            except:
                hash_value = ""
        
        return hash_value
    
    #ファイルリスト取得機能
    def file_list(self, tgt_repository):
        ret_list=[]
        if (tgt_repository == common.SERVER_REPOSITORY):
            try:
                path_list = glob.glob(self.server_repository_path + "/**", recursive=True)
                for tmp_path in path_list:
                    if not(os.path.isdir(tmp_path)):
                        #fileのみリストに追加
                        ret_list.append(str(Path(tmp_path).resolve().relative_to(self.server_repository_path)))                        
            except:
                ret_list=[]
        elif (tgt_repository == common.CLIENT_REPOSITORY):
            try:
                path_list = glob.glob(self.client_repository_path + "/**", recursive=True)
                for tmp_path in path_list:
                    if not(os.path.isdir(tmp_path)):
                        #fileのみリストに追加
                        ret_list.append(str(Path(tmp_path).resolve().relative_to(self.client_repository_path)))
            except:
                ret_list=[]

        return ret_list
