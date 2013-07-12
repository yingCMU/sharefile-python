import urllib.request, urllib.error, urllib.parse, urllib.request, urllib.parse, urllib.error
import json
import os



"""
Copyright (c) 2013 Citrix Systems, Inc.

Permission is hereby granted, free of charge, to any person obtaining a 
copy of this software and associated documentation files (the "Software"),
to deal in the Software without restriction, including without limitation 
the rights to use, copy, modify, merge, publish, distribute, sublicense, 
and/or sell copies of the Software, and to permit persons to whom the 
Software is furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in 
all copies or substantial portions of the Software.
 
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR 
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, 
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE 
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER 
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING 
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS
IN THE SOFTWARE.
"""

"""
The functions in this file will make use of the ShareFile API to perform some
of the basic operations.  Please see api.sharefile.com for more information.
 
Functions were tested with Python 2.7.3
 
Requirements:

poster module for multipart/form upload, see http://pypi.python.org/pypi/poster/

Optional parameters can be passed to functions as a dictionary as follows:

ex: 
 
users_create('mysubdomain', 'mytopleveldomain', 'myauthid',          # required parameters 
             'firstname', 'lastname', 'an@email.address', False,     # required parameters
             {'company':'ACompany',                                  # optional parameter 
              'password':'Apassword', 
              'notify':True, 
              'canviewmysettings':False})
 
See api.sharefile.com for optional parameter names for each operation.
"""

def authenticate( username, password):
    """Calls getAuthID to retrieve an authid that will be used for subsequent calls to API. 
    
    If you normally login to ShareFile at an address like https://mycompany.sharefile.com
    then you will call this function like: 
    
    authenticate('mycompany', 'sharefile.com', 'my@user.name', 'mypassword')
    
    and you will be returned an authid or in the case of failure None.  The error code
    and error message will also be output.
    
    Args:
        string subdomain
        string tld 
        string username
        string password
    Return:
        an authId string or None if failure
    """
    
    # parameter dictionary
    url_params = {'username':username, 'password':password, 'fmt':'json'}
    
    # construct url
    url = 'https://%s.%s/rest/getAuthID.aspx?%s'%("electric-cloud", "sharefile.com", urllib.parse.urlencode(url_params))
    
    authid = None
    rawresponse = urllib.request.urlopen(url).read().decode("utf-8")
    print ("begin")
    print (rawresponse)
    print ("end")
    try:
        response = json.loads(rawresponse)
        # the response will either be returned with errod=False (no error) and include
        # a value, or error=True and include an errorCode and errorMessage
        if not response['error']:
            authid = response['value']
        else:
            print(('Error %d : %s'%(response['errorCode'], response['errorMessage'])))
    except urllib.error.HTTPError as ex_http:
        print (ex_http)
    
    return authid

def folder_list(subdomain, tld, authid, path='/'):
    """ Prints out a folder list for the specified path or root if none is provided.
    
    Currently prints out id, filename, creationdate, type.  Uncomment the 'print response'
    line to see the entire response.
    
    Args:
        string subdomain
        string tld
        string authid
        string path folder to list
    """
    url_params = {'authid':authid, 'fmt':'json', 'op':'list', 'path':path}
    
    url = 'https://%s.%s/rest/folder.aspx?%s'%(subdomain, tld, urllib.parse.urlencode(url_params))

    try:
        response = json.loads(urllib.request.urlopen(url).read().decode("utf-8"))

        if not response['error']:
            #print response
            for item in response['value']:
                print(('%s %s %s %s'%(item['id'], item['filename'], item['creationdate'], item['type'])))
        else:
            print(('Error %d : %s'%(response['errorCode'], response['errorMessage'])))
            
    except urllib.error.HTTPError as ex_http:
        print (ex_http)

def folder_create(authid, path,name):
    """ Prints out a folder list for the specified path or root if none is provided.
    
    Currently prints out id, filename, creationdate, type.  Uncomment the 'print response'
    line to see the entire response.
    
    Args:
        string subdomain
        string tld
        string authid
        string path folder to list
    """
    
    url_params = {'authid':authid, 'fmt':'json', 'op':'create', 'path':path, 'name':name}
    
    url = 'https://%s.%s/rest/folder.aspx?%s'%("electric-cloud", "sharefile.com", urllib.parse.urlencode(url_params))

    try:
        response = json.loads(urllib.request.urlopen(url).read().decode("utf-8"))

        if not response['error']:
             print ("folder "+path+"/"+name+" created")
             print (response)
        else:
            print(('Error %d : %s'%(response['errorCode'], response['errorMessage'])))
            
    except urllib.error.HTTPError as ex_http:
        print (ex_http)
        
def folder_grant(authid, path,email):
    """ Prints out a folder list for the specified path or root if none is provided.
    
    Currently prints out id, filename, creationdate, type.  Uncomment the 'print response'
    line to see the entire response.
    
    Args:
            authid<s>
            id<s> or path<s>
            userid<s> or email<s>
            download<b> (true)
            upload<b> (false)
            view<b> (true)

        string authid
        string path folder to list
        
    """
    
    url_params = {'authid':authid, 'fmt':'json', 'op':'grant', 'path':path, 'email':email}
    optional_parameters = {'download': True, 'upload': True, 'view' : True}
    url_params.update(optional_parameters)
    url = 'https://%s.%s/rest/folder.aspx?%s'%("electric-cloud", "sharefile.com", urllib.parse.urlencode(url_params))
   
    try:
        response = json.loads(urllib.request.urlopen(url).read().decode("utf-8"))

        if not response['error']:
             print ("folder "+path+" granted to user "+email)
             print (response)
        else:
            print(('Error %d : %s'%(response['errorCode'], response['errorMessage'])))
            
    except urllib.error.HTTPError as ex_http:
        print (ex_http)



    
def users_create( authid, firstname, lastname, email, isemployee):
    """ Create a client or employee user in ShareFile.
    
    Args:
        string subdomain
        string tld
        string authid
        string firstname
        string lastname
        string email
        boolean isemployee true to create an employee, false to create a client
        dictionary optional_parameters see api.sharefile.com for optional parameter names
    """
    url_params = {'authid':authid, 'fmt':'json', 'op':'create', 'firstname':firstname, 'lastname':lastname, 'email':email, 'isemployee':isemployee}
    #url_params.update(optional_parameters)
    
    url = 'https://%s.%s/rest/users.aspx?%s'%("electric-cloud", "sharefile.com", urllib.parse.urlencode(url_params))
    #print (url)

    try:
        response = json.loads(urllib.request.urlopen(url).read().decode("utf-8"))
        if not response['error']:
            print("new user "+email +" created")
            print (response)
        else:
            print(('Error %d : %s'%(response['errorCode'], response['errorMessage'])))
            
    except urllib.error.HTTPError as ex_http:
        print (ex_http)
        
def group_list( authid, targetName):
    """ Prints out a folder list for the specified path or root if none is provided.
    
    Currently prints out id, filename, creationdate, type.  Uncomment the 'print response'
    line to see the entire response.
    
    Args:
        string subdomain
        string tld
        string authid
        string path folder to list
    """
    url_params = {'authid':authid, 'fmt':'json', 'op':'list'}
    
    url = 'https://%s.%s/rest/group.aspx?%s'%("electric-cloud", "sharefile.com",urllib.parse.urlencode(url_params))

    try:
        response = json.loads(urllib.request.urlopen(url).read().decode("utf-8"))

        if not response['error']:
            #print (response)
            for item in response['value']:
                if  item['name'] == targetName:
                    #print(('%s %s '%(item['id'], item['name'])))
                    return item['id']
                  
        else:
            print(('Error %d : %s'%(response['errorCode'], response['errorMessage'])))
            
    except urllib.error.HTTPError as ex_http:
        print (ex_http)

def group_create(subdomain, tld, authid, name, optional_parameters = {}):
    """ Create a distribution group in ShareFile.
    
    Ex: to create a group and add users to it at the same time

    group_create('mysubdomain', 'mytld', 'myauthid',         # required parameters
                 'mygroupname',                              # required parameters
                 {'isshared':True, 
                  'contacts':
                      ['user@email.address','another@email.address']}) # optional parameters
    
    Args:
        string subdomain
        string tld
        string authid
        string name
        dictionary optional_parameters see api.sharefile.com for optional parameter names
    """
    
    url_params = {'authid':authid, 'fmt':'json', 'op':'create', 'name':name}
    
    if 'contacts' in optional_parameters:
        optional_parameters['contacts'] = ','.join(optional_parameters['contacts'])
    
    url_params.update(optional_parameters)
    
    url = 'https://%s.%s/rest/group.aspx?%s'%(subdomain, tld, urllib.parse.urlencode(url_params))
    print (url)

    try:
        response = json.loads(urllib.request.urlopen(url).read().decode("utf-8"))
        if not response['error']:
            print (response)
        else:
            print(('Error %d : %s'%(response['errorCode'], response['errorMessage'])))
            
    except urllib.error.HTTPError as ex_http:
        print (ex_http)
def group_addcontacts(authid, contacts,id):
    """    
    Adds a single user or comma separated list of users to a distribution group.
     Users can be either an id or email address.    
    Args:
      authid<s>
      id<s>
      contacts<l>
    """
    
    url_params = {'authid':authid, 'fmt':'json', 'op':'addcontacts', 'contacts':contacts,'id':id}
    
   
    
    url = 'https://%s.%s/rest/group.aspx?%s'%("electric-cloud", "sharefile.com", urllib.parse.urlencode(url_params))
    #print (url)

    try:
        response = json.loads(urllib.request.urlopen(url).read().decode("utf-8"))
        if not response['error']:
            print("user "+contacts+" added to groupId "+id )
            print (response)
        else:
            print(('Error %d : %s'%(response['errorCode'], response['errorMessage'])))
            
    except urllib.error.HTTPError as ex_http:
        print (ex_http)

def search(subdomain, tld, authid, query, optional_parameters = {}):
    """ Search for items in ShareFile.
    
    Args:
        string subdomain
        string tld
        string authid
        string query
        dictionary optional_parameters see api.sharefile.com for optional parameter names
    """
    url_params = {'authid':authid, 'fmt':'json', 'op':'search', 'query':query}
    url_params.update(optional_parameters)

    url = 'https://%s.%s/rest/search.aspx?%s'%(subdomain, tld, urllib.parse.urlencode(url_params))
    print (url)

    try:
        response = json.loads(urllib.request.urlopen(url).read().decode("utf-8"))
        if not response['error']:
            print (response)
            for item in response['value']:
                path = '/'
                if item['parentid'] == 'box':
                    path = '/File Box'
                else:
                    path = item['parentsemanticpath']
                print(('%s/%s %s %s'%(path, item['filename'], item['creationdate'], item['type'])))
        else:
            print(('Error %d : %s'%(response['errorCode'], response['errorMessage'])))
            
    except urllib.error.HTTPError as ex_http:
        print (ex_http)
        
if __name__ == '__main__':
    authid = authenticate('mysubdomain', 'sharefile.com', 'my@email.address', 'mypassword')
    if authid:
        folder_list('mysubdomain', 'sharefile.com', authid, '/MyFolder') 
    