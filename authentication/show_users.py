

def show_user_name(request):

    username = request.user.username

    name = username.split('@')[0]


    return {'name_of_user':name}

