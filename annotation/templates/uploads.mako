<%inherit file="base.mako"/>

<%block name="title">- Annotations from DB</%block>
<%block name="header">Annotations from DB</%block>

<div class="row">
    <p>
        To view annotations in database they must first be uploaded.
    </p>
    <p>
        Annotations can be uploaded with the 'GPS Annotation service'.
    </p>
    <p>
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
    <p>
        Available trackers in table:
    </p>
    <ul>
        % for tracker in trackers:
        <li>
            <a class="btn btn-default" href="${request.route_path('upload.html', table=table, tracker=tracker['id'])}">${tracker['id']}, ${tracker['start']} - ${tracker['end']}</a>
        </li>
        % endfor
    </ul>
</div>
