function loadTrackerAndAnnotation(classes, annotationsUrl) {
	var ctrl = TrackAnnot.getApplication().getController('Main');
	ctrl.getClassificationsStore().loadRawData(classes);
    ctrl.getAnnotationsStore().enableRemoteMode(annotationsUrl);
}