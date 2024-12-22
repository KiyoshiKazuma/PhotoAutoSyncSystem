import command
import common

server_repository_path = "C:\\Users\\makiy\\programing\\python\\PhotoAutoSyncSystem\\src\\test\\server"
client_repository_path = "C:\\Users\\makiy\\programing\\python\\PhotoAutoSyncSystem\\src\\test\\client"

cmd=command.cmd(server_repository_path,client_repository_path)

client_files = cmd.file_list(common.CLIENT_REPOSITORY)

print(client_files)

ret = cmd.folder_add(common.SERVER_REPOSITORY, "2019/03")
filetmp = client_files[0]
ret = cmd.file_copy(common.CLIENT_REPOSITORY, filetmp)