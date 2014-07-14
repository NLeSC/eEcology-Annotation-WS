<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>Annotation - table selector</title>
</head>
<body>
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
