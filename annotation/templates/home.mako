<!DOCTYPE html>
<html>
    <head>
        <meta charset="utf-8">
        <title>Annotation</title>
        <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.2.0/css/bootstrap.min.css">
    </head>
    <body>
        <div class="page-header">
                <h1>eEcology Annotation tool</h1>
        </div>

        <div class="container">
            <div class="row jumbotron">
                <div class="col-md-6">
                    <h2>Custom</h2>
                    <p>Any tracker and time range, annotations can be loaded/saved as files</p>
                    <a class="btn btn-primary btn-lg" href="${request.static_path('annotation:static/TrackAnnot/')}" role="button">Start</a>
                </div>
                <div class="col-md-6">
                    <h2>Annotations from DB</h2>
                    <p>View annotations based on db table, uploaded using <a href="https://services.e-ecology.sara.nl/cgi-bin/flysafe/uva_admin/upload_csv.cgi">GPS Annotation service</a></p>
                    <a class="btn btn-primary btn-lg" href="${request.route_path('uploads.html')}" role="button">Start</a>
                </div>
            </div>
            <h1>Features</h1>
            <div class="row">
                <div class="col-md-4">
                    <h2>Temporal</h2>
                    <p>View tracker data in selected time range</p>
                    <p>Slide current time as red marker over range</p>
                    <p>UTC timezone everywhere</p>
                </div>
                <div class="col-md-4">
                    <h2>Spatial</h2>
                    <p>Location of GPS tracker plotted in 3D and 2D.</p>
                    <p>Using <a href="http://www.cesiumjs.org">Cesium</a> or <a href="http://earth.google.com">Google Earth</a> or <a href="http://maps.google.com">Google Maps</a></p>
                </div>
                <div class="col-md-4">
                    <h2>Acceleration</h2>
                    <p>3 axis acceleration burst of a GPS fix</p>
                </div>
            </div>
            <div class="row">
                <div class="col-md-4">
                    <h2>Tracker</h2>
                    <p>Data from tracker like direction, speed and temperature plotted as line charts.</p>
                </div>
                <div class="col-md-4">
                    <h2>Annotations</h2>
                    <p>Create, edit and view annotations. </p>
                    <p>Annotations are shown by label color in each visualization</p>
                </div>
                <div class="col-md-4">
                    <h2>Video integration</h2>
                    <p>Annotation using a syncronized video. Video can be uploaded or supplied as url.</p>
                </div>
            </div>
        </div>
    </body>
</html>
