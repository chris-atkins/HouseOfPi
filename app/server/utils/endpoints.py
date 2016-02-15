from flask import url_for  # @UnresolvedImport

def listEndpoints(app):
    output = []
    for rule in app.url_map.iter_rules():
        options = {}
        for arg in rule.arguments:
            options[arg] = "[{0}]".format(arg)
     
        methods = ','.join(rule.methods)
        url = url_for(rule.endpoint, **options)
        line = "{:50s} {:20s} {}".format(rule.endpoint, methods, url)
        line += '<br/>'
        output.append(line)
    
    return output
