function loadTrackerAndAnnotation(tableName, trackerId) {

    var url = '/aws/uploads/' + tableName + '/meta.json';
    ctrl.getTrackerId().getStore().getProxy().url = url;
    Ext.Ajax.request({
        url: url,
        success: function(response) {
             data = Ext.decode(response.responseText);
             var ctrl = TrackAnnot.getApplication().getController('Main');
             ctrl.getClassificationsStore().loadRawData(data.classifications);
             var tracker = data.trackers[0];
             ctrl.getTrackerId().setValue(tracker.id);
             ctrl.setTrackRange(tracker.start, tracker.end);
             var button = Ext.ComponentQuery.query('button[action=loadTrack]')[0];
             ctrl.trackStore.on('load', function(store, data, isLoaded) {
                 Ext.Ajax.request({
                    url: tracker.annotations,
                    success: function(aresponse) {
                        var astore = ctrl.getAnnotationsStore();
                        astore.removeAll();
                        astore.importText(aresponse.responseText, ctrl.trackStore);
                    }
                 });

             }, this, {single: true});

             ctrl.loadTrack(button);
        }
    });
}