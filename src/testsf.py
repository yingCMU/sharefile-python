import sharefile
print("hello world")
name = "testORG"
email = "email@gamil.com"
targetName = 'Accelerator and Insight clients'
gid = 'gd971713-5082-4cf8-8350-b02e2b891989'
#authid = sharefile.authenticate( 'yli@electric-cloud.com', '0814Cmu$')
authid = "nmc2143ali2vvbodhwfvd1sp"

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

'''
sharefile.group_addcontacts(authid, email, gid)