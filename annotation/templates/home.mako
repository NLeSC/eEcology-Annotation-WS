<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>Annotation - </title>
</head>
<body>
<h1>Annotation tool</h1>
<span>Annotation can be viewed and edited in 2 ways:</span>
<ul>
<li><a href="${request.static_path('annotation:static/TrackAnnot/')}">Way one</a>, Any tracker and time range, annotations can be loaded/saved manually</li>
<li><a href="${request.route_path('uploads.html')}">Way two</a>, view annotations based on db table, uploaded using <a href="https://services.e-ecology.sara.nl/cgi-bin/flysafe/uva_admin/upload_csv.cgi">GPS Annotation service</a></li>
</ul>
</body>
</html>
