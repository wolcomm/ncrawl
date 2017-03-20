$(document).ready(function () {

    // shout about v6
    var ipver = $("#ip-version").text();
    if (ipver == "IPv4") {
        $("#legacy-ip-modal").modal();
    }

    var svg = d3.select("#topology-container")
        .append("svg")
        .style("min-height", "600");
    var width = $("svg").width(),
        height = $("svg").height();
    var radius = {
        inner: 14,
        outer: 16
    };
    var icons = {
        router: "\ue61c"
    };

    var simulation = d3.forceSimulation()
        .force("link", d3.forceLink()
            .id(function (d) {
                return d.name;
            })
            // .distance(function (d) {
            //     return d.distance;
            // })
        )
        .force("charge", d3.forceManyBody().strength(function () {
            return -30;
        }))
        .force("collide", d3.forceCollide().radius(function () {
            return radius.outer * 2;
        }))
        .force("center", d3.forceCenter(width / 2, height / 2));

    d3.json("/topology/lldp/", function (error, graph) {
        if (error) throw error;

        var link = svg.append("g")
            .attr("class", "links")
            .selectAll("line")
            .data(graph.links)
            .enter().append("line")
            .style("stroke-width", function (d) {
                return Math.log10(d.bandwidth) + 1;
            });

        var node = svg.append("g")
            .attr("class", "nodes")
            .selectAll("g")
            .data(graph.nodes)
            .enter()
            // .append("circle")
            // .attr("r", radius)
            .append("g")
            .attr("class", "node")
            .call(d3.drag()
                .on("start", dragstarted)
                .on("drag", dragged)
                .on("end", dragended));

        node.append("circle")
            .attr("r", radius.outer);

        node.append("text")
            .style("font-size", function (d) {
                return 2 * radius.inner + "px";
            })
            .text(function (d) {
                return icons[d.icon];
            });

        node.append("title")
            .text(function (d) {
                return d.name;
            });

        simulation
            .nodes(graph.nodes)
            .on("tick", ticked);

        simulation.force("link")
            .links(graph.links);

        function ticked() {
            node.selectAll("circle")
                .attr("cx", function (d) {
                    return d.x = Math.max(radius.outer, Math.min(d.x, width - radius.outer));
                })
                .attr("cy", function (d) {
                    return d.y = Math.max(radius.outer, Math.min(d.y, height - radius.outer));
                });
            node.selectAll("text")
                .attr("transform", function (d) {
                    return "translate(" + (d.x - radius.inner) + "," + (d.y + radius.inner) + ")";
                });
            link
                .attr("x1", function (d) {
                    return d.source.x;
                })
                .attr("y1", function (d) {
                    return d.source.y;
                })
                .attr("x2", function (d) {
                    return d.target.x;
                })
                .attr("y2", function (d) {
                    return d.target.y;
                });

        }
    });

    function dragstarted(d) {
        if (!d3.event.active) simulation.alphaTarget(0.3).restart();
        d.fx = d.x;
        d.fy = d.y;
    }

    function dragged(d) {
        d.fx = d3.event.x;
        d.fy = d3.event.y;
    }

    function dragended(d) {
        if (!d3.event.active) simulation.alphaTarget(0);
        d.fx = null;
        d.fy = null;
    }

});