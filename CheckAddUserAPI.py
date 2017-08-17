from APIs import *
from Mi_Functions import *
from random import choice
from string import lowercase

log_csv='AddUserApiResult.csv'
url='https://test.hpenv.com/rest/v1/users'
user='hpemkt'
password='sfT@45Gh'


def GENERATE_STRING_BY_SIZE(size):
    string_val = "".join(choice(lowercase) for i in range(size))
    return string_val

DELETE_LOG_CONTENT(log_csv)

### Add user ###
json={"email":"hren@hpe.com", "firstName":"Hren", "lastName":"Morjoviy2", "company":"HPE", "country":"Israel"}
result=ADD_NEW_USER(url,user,password,json)
print '-'*100
for k in result:
    if k=='Response_Headers':
        print '\r\n### '+k+' ###'
        for h in result[k]:
            print h+':'+result[k][h]
        print '\r\n'
    else:
        print k,' --> ', result[k]
print '-'*100

# ### Bad request ###
# ### Add user ###
# json={"emailZZZZZZZZZZZZZ":"hren@hpe.com", "firstName":"Hren", "lastName":"Morjoviy2", "company":"HPE", "country":"Israel"}
# result=ADD_NEW_USER(url,user,password,json)
# print '-'*100
# for k in result:
#     if k=='Response_Headers':
#         print '\r\n### '+k+' ###'
#         for h in result[k]:
#             print h+':'+result[k][h]
#         print '\r\n'
#     else:
#         print k,' --> ', result[k]
# print '-'*100




# ### Unauthorized error ###
# user='hpemkt+ZZZZZZZZZZZZ'
# json={"email":"hren@hpe.com", "firstName":"Hren", "lastName":"Morjoviy2", "company":"HPE", "country":"Israel"}
# result=ADD_NEW_USER(url,user,password,json)
# print '-'*100
# for k in result:
#     if k=='Response_Headers':
#         print '\r\n### '+k+' ###'
#         for h in result[k]:
#             print h+':'+result[k][h]
#         print '\r\n'
#     else:
#         print k,' --> ', result[k]
# print '-'*100


# ### Add the same user in loop ###
# json={"email":"hren@hpe.com", "firstName":"Hren", "lastName":"Morjoviy", "company":"HPE", "country":"Israel"}
# for x in range(0,100):
#     result=ADD_NEW_USER(url,user,password,json)
#     print '-'*100
#     for k in result:
#         if k=='Response_Headers':
#             print '\r\n### '+k+' ###'
#             for h in result[k]:
#                 print h+':'+result[k][h]
#             print '\r\n'
#         else:
#             print k,' --> ', result[k]
#     print '-'*100


# ### Add a new user in loop ###
# for x in range(0,10):
#     email=GENERATE_STRING_BY_SIZE(5)+'.'+GENERATE_STRING_BY_SIZE(8)+'@'+GENERATE_STRING_BY_SIZE(5)+'.'+GENERATE_STRING_BY_SIZE(3)
#     f_name='ZABABUN'
#     l_name=GENERATE_STRING_BY_SIZE(8)
#     company=GENERATE_STRING_BY_SIZE(7)
#     country=GENERATE_STRING_BY_SIZE(6)
#     json={"email":email, "firstName":f_name, "lastName":l_name, "company":company, "country":country}
#     result=ADD_NEW_USER(url,user,password,json)
#     print '-'*100
#     for k in result:
#         if k=='Response_Headers':
#             print '\r\n### '+k+' ###'
#             for h in result[k]:
#                 print h+':'+result[k][h]
#             print '\r\n'
#         else:
#             print k,' --> ', result[k]
#     print '-'*100