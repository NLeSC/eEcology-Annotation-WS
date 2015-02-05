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
    <form method="GET" role="form">
        <label for="table">Table (schema.table):</label>
        <input name="table" size="60" value="${table}">
        <input class="btn btn-default" type="submit"/>
    </form>
</div>
<div class="row">
    <p>
        Available trackers in table:
    </p>
    <table class="table table-hover">
    <thead>
    <tr>
    <th>ID</th>
    <th>Start</th>
    <th>End</th>
    <th>Action</th>
    </tr>
    </thead>
    <tbody>
        % for tracker in trackers:
        <tr>
           <td>${tracker['id']}</td>
           <td>${tracker['start']}</td>
           <td>${tracker['end']}</td>
           <td>
           % if tracker['size'] > tracker['page_size']:
           <a class="btn btn-primary" href="${request.route_path('annotations.html', table=table, _query=dict(id=tracker['id'], start=tracker['start'].isoformat(), end=tracker['first_page'].isoformat()))}" title="Visualize from ${tracker['start'].isoformat()} to ${tracker['first_page'].isoformat()}">
           <span class="glyphicon glyphicon-eye-open"></span> First ${tracker['page_size']} annotations</a>
           <a class="btn btn-primary" href="${request.route_path('annotations.html', table=table, _query=dict(id=tracker['id'], start=tracker['last_page'].isoformat(), end=tracker['end'].isoformat()))}" title="Visualize from ${tracker['last_page'].isoformat()} to ${tracker['end'].isoformat()}">
           <span class="glyphicon glyphicon-eye-open"></span> Last ${tracker['page_size']} annotations</a>
           <a class="btn btn-warning" href="${request.route_path('annotations.html', table=table, _query=dict(id=tracker['id'], start=tracker['start'].isoformat(), end=tracker['end'].isoformat()))}" title="Visualize all annotations, visualization might not be able to show all the data">
           <span class="glyphicon glyphicon-eye-open"></span> All ${tracker['size']} annotations</div></a>
           % else:
           <a class="btn btn-primary" href="${request.route_path('annotations.html', table=table, _query=dict(id=tracker['id'], start=tracker['start'].isoformat(), end=tracker['end'].isoformat()))}" title="Visualize all annotations">
           <span class="glyphicon glyphicon-eye-open"></span> All annotations</a>
           % endif
           <a class="btn btn-default" href="${request.route_path('annotations.csv', table=table, _query=dict(id=tracker['id'], start=tracker['start'].isoformat(), end=tracker['end'].isoformat()))}" title="Download CSV">
           <span class="glyphicon glyphicon-download"></span></a>
           </td>
        </tr>
        % endfor
    </tbody>
    </table>
</div>
