import sharefile
import sys




authid = sys.argv[1]
email = sys.argv[2]

org = sys.argv[3]




#grant folder
path = "/clients/"+org  
sharefile.folder_grant(authid, path, email)
path = "/clients/"+org+"/uploads"
sharefile.folder_grant(authid, path, email)
path = "/clients/"+org+"/licenses"
sharefile.folder_grant(authid, path, email)

