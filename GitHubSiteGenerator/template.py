HEADER = \
'''
<!DOCTYPE html>
<html>
    <head>
        <title>%s</title>
        <meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1">
        <link rel="stylesheet" href="/css/bootstrap-theme.min.css" type="text/css" />
        <link rel="stylesheet" href="/css/bootstrap.min.css" type="text/css" />
        <link rel="stylesheet" href="/css/bootstrap-treeview.min.css" type="text/css" />

        <script type="text/javascript" src="/js/bootstrap.min.js" ></script>
        <script type="text/javascript" src="/js/jquery-2.1.4.min.js" ></script>
        <script type="text/javascript" src="/js/bootstrap-treeview.min.js" ></script>
        <script type="text/javascript" src='https://cdn.mathjax.org/mathjax/latest/MathJax.js?config=TeX-AMS-MML_HTMLorMML'></script>

        <nav class="navbar navbar-default">
            <div class="container-header">
                <a class="navbar-brand" href="#">Maxiee笔记</a>
            </div>
        </nav>

    </head>
'''

BODY = \
'''
<body>
        <div class="page container">
            <div class="row">
                <div class="col-sm-3">
                    <div id="tree"></div>
                </div>
                <div class="col-sm-8">
                   %s 
                </div>
            </div>
        </div>
    </body>
    <script type="text/javascript" src="/js/content.js" ></script>
    <script type="text/javascript">
    $('#tree').treeview({data: tree, enableLinks: true});
    </script>
</html>
'''
