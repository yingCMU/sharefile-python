import sharefile
import sys



email = sys.argv[1]
password = sys.argv[2]
authid = sharefile.authenticate( email, password)

print (authid)
#create 3 folders
'''
path = "/clients"
sharefile.folder_create(authid, path, name)
path = "/clients/"+name
sharefile.folder_create(authid, path, "uploads")
sharefile.folder_create(authid, path, "licenses")

#create new user

sharefile.users_create(authid, "firstname", "lastname", email, False)


#grant folder
path = "/clients/"+name
sharefile.folder_grant(authid, path, email)
path = "/clients/"+name+"/uploads"
sharefile.folder_grant(authid, path, email)
path = "/clients/"+name+"/licenses"
sharefile.folder_grant(authid, path, email)


gid = sharefile.group_list(authid,targetName)
print ("targetName : id-"+gid)


sharefile.group_addcontacts(authid, email, gid)
'''