import sharefile
import sys



org = sys.argv[2]

authid = sys.argv[1]
print("org "+org)
print ("authid "+authid)
#create 3 folders

path = "/clients"
sharefile.folder_create(authid, path, org)
path = "/clients/"+org
sharefile.folder_create(authid, path, "uploads")
sharefile.folder_create(authid, path, "licenses")
