<!DOCTYPE html>
<html>
    <head>
        <meta charset="utf-8">
        <title>eEcology Annotation tool <%block name="title"/></title>
        <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.2.0/css/bootstrap.min.css">
        <style>
            body {
                padding-bottom: 70px;
            }
        </style>
    </head>
    <body>
        <div class="page-header">
            <h1>eEcology Annotation tool</h1>
            <h2 class="text-muted"><%block name="header"/></h2>
        </div>

        <div class="container">
            ${self.body()}
        </div>

        <nav class="navbar navbar-default navbar-fixed-bottom" role="navigation">
            <div class="container">
                <p class="text-muted">
                    eEcology Annotation tool is a virtual lab of <a target="_blank" href="http://www.uva-bits.nl">UvA-BiTS</a>,
                    &copy; <a target="_blank" href="http://www.esciencecenter.nl">Netherlands eScience Center</a> 2014
                </p>
            </div>
        </nav>
    </body>
</html>
