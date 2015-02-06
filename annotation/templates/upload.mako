<% appbase = request.static_path('annotation:static/TrackAnnot/') %>
<!DOCTYPE HTML>
<html>
<head>
<meta charset="UTF-8">
<title>TrackAnnot</title>
<link rel="stylesheet" href="${appbase}resources/app.css">
<link rel="stylesheet" href="${appbase}resources/libs/Cesium-1.4/Build/Cesium/Widgets/widgets.css">
<!--
See https://developers.google.com/loader/#AutoLoading
Convert:
google.load("earth", "1");
google.load("maps", "3.xx", {other_params:"sensor=false"});
to:
{"modules":[{"version":"1","name":"earth"},{"version":"3.xx","other_params":"sensor=false","name":"maps"}]}
and append after 'https://www.google.com/jsapi?autoload=' in url encoded format.
 -->
<script type="text/javascript" src="https://www.google.com/jsapi?autoload=%7B%22modules%22%3A%5B%7B%22version%22%3A%221%22%2C%22name%22%3A%22earth%22%7D%2C%7B%22version%22%3A%223.xx%22%2C%22other_params%22%3A%22sensor%3Dfalse%22%2C%22name%22%3A%22maps%22%7D%5D%7D"></script>
<script type="text/javascript" src="${appbase}resources/libs/d3/d3.min.js"></script>
<script type="text/javascript"  src="${appbase}resources/libs/Cesium-1.4/Build/Cesium/Cesium.js"></script>

<link rel="stylesheet" href="${appbase}resources/TrackAnnot-all.css"/>
<script type="text/javascript" src="${appbase}app.js"></script>
<script type="text/javascript" src="${request.static_path('annotation:static/table.js')}"></script>
<script type="text/javascript">
Ext.onReady(function() {
    loadTrackerAndAnnotation(${classes | n}, '${annotations_url}');
});
</script>
</head>
<body></body>
</html>
