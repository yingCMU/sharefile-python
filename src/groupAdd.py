import sharefile
import sys



email = sys.argv[2]

authid = sys.argv[1]

groupName = sys.argv[3]



gid = sharefile.group_list(authid,groupName)
print ("target group Name : " + groupName+" ;id is  "+gid)


sharefile.group_addcontacts(authid, email, gid)
