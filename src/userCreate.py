import sharefile
import sys




authid = sys.argv[1]
email = sys.argv[2]

firstname = sys.argv[3]
lastname = sys.argv[4]


#create new user

sharefile.users_create(authid, firstname, lastname, email, False)

