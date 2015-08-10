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
        <link rel="stylesheet" href="/css/github.css">
        <link rel="stylesheet" href="/css/jqtree.css">

        <script type="text/javascript" src="/js/bootstrap.min.js" ></script>
        <script type="text/javascript" src="/js/jquery-2.1.4.min.js" ></script>
        <script type="text/javascript" src="/js/tree.jquery.js"></script>
        <script type="text/javascript" src="/js/js.cookie.js"></script>
        <script type="text/javascript" src='https://cdn.mathjax.org/mathjax/latest/MathJax.js?config=TeX-AMS-MML_HTMLorMML'></script>
        <script src="//cdnjs.cloudflare.com/ajax/libs/highlight.js/8.6/highlight.min.js"></script>

        <nav class="navbar navbar-default">
            <div class="container-header">
                <a class="navbar-brand" href="#">Maxiee笔记</a>
            </div>
            <div id="navbar" class="navbar-collapse collapse">
                <ul class="nav navbar-nav">
                    <li><a href="http://maxiee.github.io/static/html/resume.html">我的简历</a></li>
                </ul>
            </div>
        </nav>

    </head>
'''

BODY = \
'''
<body>
        <div class="container-fluid">
            <div class="row">
                <div class="col-sm-3">
                    <div id="tree"></div>
                </div>
                <div class="col-sm-9" id="content">
                   %s 
                </div>
            </div>
        </div>
    <script type="text/javascript" src="/js/content.js" ></script>
    <script type="text/javascript">
    $('#tree').tree({
        data: data, 
        autoEscape: false,
        autoOpen: true,
        saveState: true,
        closedIcon: '+',
        openedIcon: '-'
    });
    $('table').addClass('table table-striped');
    </script>
    <script>hljs.initHighlightingOnLoad();</script>
</body>
</html>
'''
