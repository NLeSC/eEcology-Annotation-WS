<!DOCTYPE html>
<html>
    <head>
        <meta charset="utf-8">
        <title>Annotation - Select annotation table</title>
        <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.2.0/css/bootstrap.min.css">
    </head>
    <body>
        <div class="page-header">
            <h1>eEcology Annotation tool</h1>
            <h2>Select annotation table</h2>
        </div>
        <div class="container">
            <div class="row">
                <p>
                    To view annotations in database they must first be uploaded.
                </p>
                <p>
                    Annotations can be uploaded with the 'GPS Annotation service'.
                </p><p>
                    Use the '<b>acceleration classification</b>' template in the <a href="https://services.e-ecology.sara.nl/cgi-bin/flysafe/uva_admin/upload_csv.cgi">GPS Annotation service</a>.
                </p>
            </div>

            <div class="row">
            <form method="POST" role="form">
                <label for="table">Table (schema.table):</label>
                <input name="table" size="60" value="${table}">
                <input class="btn btn-default" type="submit"/>
            </form>
            </div>
            <div class="row">
            <p>Trackers in annotation table:</p>
            <ul>
                % for tracker in trackers:
                <li>
                    <a class="btn btn-default" href="${request.route_path('upload.html', table=table, tracker=tracker['id'])}">${tracker['id']}, ${tracker['start']} - ${tracker['end']}</a>
                </li>
                % endfor
            </ul>
            </div>
        </div>
    </body>
</html>
