<%inherit file="base.mako"/>

<div class="row jumbotron">
    <div class="col-md-6">
        <h2>Annotations from DB</h2>
        <p>
            View annotations from a table in the eEcology Database
        </p>
        <a class="btn btn-primary btn-lg" href="${request.route_path('uploads.html')}" role="button">Start</a>
    </div>
    <div class="col-md-6">
        <h2>Start from scratch</h2>
        <p>
            Any tracker and time range, annotations can be loaded/saved as files
        </p>
        <a class="btn btn-primary btn-lg" href="${request.static_path('annotation:static/TrackAnnot/')}" role="button">Start</a>
    </div>
</div>
<h1>Features</h1>
<div class="row">
    <div class="col-md-4">
        <h2>Temporal</h2>
        <p>
            View tracker data in selected time range
        </p>
        <p>
            Slide current time as red marker over range
        </p>
        <p>
            UTC timezone everywhere
        </p>
    </div>
    <div class="col-md-4">
        <h2>Spatial</h2>
        <p>
            Location of GPS tracker plotted in 3D and 2D.
        </p>
        <p>
            Using <a href="http://www.cesiumjs.org">Cesium</a> or <a href="http://earth.google.com">Google Earth</a> or <a href="http://maps.google.com">Google Maps</a>
        </p>
    </div>
    <div class="col-md-4">
        <h2>Acceleration</h2>
        <p>
            3 axis acceleration burst of a GPS fix
        </p>
        <p>
        Visualized as a movie strip.
        </p>
    </div>
</div>
<div class="row">
    <div class="col-md-4">
        <h2>Tracker</h2>
        <p>
            Data and derived data from tracker like direction, speed and temperature plotted as line charts.
        </p>
    </div>
    <div class="col-md-4">
        <h2>Annotations</h2>
        <p>
            Create, edit and view annotations.
        </p>
        <p>
            Annotations are shown by label color in each visualization
        </p>
    </div>
    <div class="col-md-4">
        <h2>Video integration</h2>
        <p>
            Annotation using a syncronized video. Video can be uploaded or supplied as url.
        </p>
    </div>
</div>
<div class="row">
    <div class="col-md-4">
        <h2>Custom data integration</h2>
        <p>
            Visualize your own data besides tracker and annotations.
        </p>
        <p>
        By uploading a CSV file.
        </p>
    </div>
</div>