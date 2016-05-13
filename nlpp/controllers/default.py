# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## This is a sample controller
## - index is the default action of any application
## - user is required for authentication and authorization
## - download is for downloading files uploaded in the db (does streaming)
#########################################################################

def index():
    return locals()
    

def search():
    import urllib
    import json
    search_query = request.vars.searchQuery.replace(' ', '+')
    page = request.args(0, cast=int) or 0
    #category = request.vars.category or "*"
    #search_result_url = "http://localhost:8983/solr/news/select?q=category%3A{}+AND+{}&start={}&wt=json&indent=true&facet=true&facet.field=category".format(category, search_query, (page-1)*10)
    search_result_url = "http://localhost:8983/solr/nlp/select?q={}&start={}&wt=json&indent=true".format(search_query, (page-1)*10)
    search_response = urllib.urlopen(search_result_url)
    search_result = json.loads(search_response.read())

    return locals()

def show_detail():
    import urllib
    import json
    id = request.args(0)
    search_result_url = "http://localhost:8983/solr/nlp/select?q={0}&df=id&wt=json&indent=true&facet=true".format(id)
    search_response = urllib.urlopen(search_result_url)
    search_result = json.loads(search_response.read())
    return locals()

def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/bulk_register
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    also notice there is http://..../[app]/appadmin/manage/auth to allow administrator to manage users
    """
    return dict(form=auth())


@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)


def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    return service()

