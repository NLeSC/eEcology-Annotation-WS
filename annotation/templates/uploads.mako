<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>Annotation - table selector</title>
</head>
<body>
Uploaded annotations in <a href="https://services.e-ecology.sara.nl/cgi-bin/flysafe/uva_admin/upload_csv.cgi">GPS Annotation service</a> should use the '<b>acceleration classification</b>' template.
<form method="POST">
<label for="table">Table (schema.table):</label>
<input name="table" size="60" value="${table}">
<input type="submit"/>
</form>
Trackers:
<ul>
% for tracker in trackers:
<li><a href="${request.route_path('upload.html', table=table, tracker=tracker['id'])}">${tracker['id']}, ${tracker['start']} - ${tracker['end']}</a></li>
% endfor
</ul>
</body>
</html>
