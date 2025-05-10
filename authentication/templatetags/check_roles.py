from django import template

register = template.Library()



# @register.simple_tag

# def lowercase(word):

#     return word.lower()
@register.simple_tag
def check_user_role(request,roles):

    roles=roles.split(',') #returns admin  as an list

    allow = False

    if request.user.role in roles:

        allow = True

    return allow    
    
