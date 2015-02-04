function loadTrackerAndAnnotation(classes, annotationsUrl) {
	var ctrl = TrackAnnot.getApplication().getController('Main');
	ctrl.getClassificationsStore().loadRawData(classes);
    ctrl.getAnnotationsStore().enableRemoteMode(annotationsUrl);
    var button = Ext.ComponentQuery.query('button[action=loadTrack]')[0];
    ctrl.loadTrack(button);
}