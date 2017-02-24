$(document).ready(function () {
    var ipver = $("#ip-version").text();
    if (ipver == "IPv4") {
        $("#legacy-ip-modal").modal();
    }
    // configure topology
    var topoConfig = {
        adaptive: true,
        dataProcessor: 'force',
        identityKey: 'name',
        nodeConfig: {
            label: 'model.name',
            iconType: 'model.icon'
        },
        nodeSetConfig: {
            label: 'model.name',
            iconType: 'router'
        },
        linkConfig: {
            linkType: 'curve'
        },
        showIcon: true
    };
    // perform data query
    var topo_src = '/topology/lldp/';
    var topo_query = $.getJSON(topo_src);
    topo_query.done(function (topoData) {
        topoConfig.data = topoData;
        // init topology and ui app
        var topo = new nx.graphic.Topology(topoConfig);
        var app = new nx.ui.Application();
        app.container(document.getElementById('topology-container'));
        topo.attach(app);
    });
});