import ldap 
import ldap.modlist as modlist

def add_user(cnn, username, passwd):
    dn="uid={0},ou=people,dc=nap,dc=com".format(username)
    attrs = {}
    attrs['objectclass'] = ['inetOrgPerson','shadowAccount']
    attrs['cn'] = username
    attrs['sn'] = username
    attrs['userPassword'] = passwd
    attrs['description'] = 'User object for replication using slurpd'
    ldif = modlist.addModlist(attrs)
    cnn.add_s(dn,ldif)


def del_user(cnn, username):
    dn="uid={0},ou=people,dc=nap,dc=com".format(username)
    try:
        cnn.delete_s(dn)
    except ldap.LDAPError, e:
        print 'failed to delete user', e

def get_user(cnn, base):
    base_dn="ou=people,dc=nap,dc=com"
    search_scope = ldap.SCOPE_SUBTREE
    retrieve_attr = None
    search_filter = "cn=*"
    try:
        ldap_res_id = cnn.search(base_dn, search_scope, search_filter, retrieve_attr)
     	result_set = []
	while cnn:
		res_type, res_data = cnn.result(ldap_res_id, 0)
		if res_data == []:
			break;
		else:
			if res_type == ldap.RES_SEARCH_ENTRY:
				result_set.append(res_data)
	for s in result_set:
		print s, '\n'
    except ldap.LDAPError, e:
        print e


if __name__ == '__main__':
    LOGIN = "cn=admin,dc=nap,dc=com"
    PASSWORD = 'cshuo'
    LDAP_URL = "ldap://172.17.0.8"
    l = ldap.initialize(LDAP_URL) 
    l.bind(LOGIN, PASSWORD) 
    #do something
    #del_user(l, 'apple')
    add_user(l, 'test', 'artemis')
    get_user(l, '')
    l.unbind_s()

