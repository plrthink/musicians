'use strict';

angular.module('visualization')
  .directive('chart', ['$timeout', function($timeout) {

    var link = function(scope, element, attrs) {

      $timeout(function() {
        // var width = 1280,
        //   height = 12000;

        // var cluster = d3.layout.cluster()
        //     .size([height, width-280]);

        // var diagonal = d3.svg.diagonal()
        //     .projection(function(d) { return [d.y, d.x]; });

        // var svg = d3.select(element[0]).append("svg")
        //     .attr("width", width)
        //     .attr("height", height)
        //     .append("g")
        //     .attr("transform", "translate(100,0)");

        // var root = scope.musicians,
        //     nodes = cluster.nodes(root),
        //     links = cluster.links(nodes);

        // var link = svg.selectAll(".link")
        //     .data(links)
        //     .enter().append("path")
        //     .attr("class", "link")
        //     .attr("d", diagonal);

        // var node = svg.selectAll(".node")
        //     .data(nodes)
        //     .enter().append("g")
        //     .attr("class", "node")
        //     .attr("transform", function(d) { return "translate(" + d.y + "," + d.x + ")"; })

        // node.append("circle")
        //     .attr("r", 4.5);

        // node.append("text")
        //     .attr("dx", function(d) { return d.children ? -8 : 8; })
        //     .attr("dy", 3)
        //     .style("text-anchor", function(d) { return d.children ? "end" : "start"; })
        //     .text(function(d) { return d.name; });

        // d3.select(self.frameElement).style("height", height + "px");

        var m = [20, 120, 20, 120],
            w = 1440 - m[1] - m[3],
            h = 12000 - m[0] - m[2],
            i = 0,
            root;

        var tree = d3.layout.tree()
            .size([h, w]);

        var diagonal = d3.svg.diagonal()
            .projection(function(d) { return [d.y, d.x]; });

        var vis = d3.select(element[0]).append("svg")
            .attr("width", w + m[1] + m[3])
            .attr("height", h + m[0] + m[2])
            .append("svg:g")
            .attr("transform", "translate(" + m[3] + "," + m[0] + ")");

        // Add tooltip div
        var tooltip = d3.select(element[0]).append("a")
        .attr("class", "tooltip")
        .style("opacity", 1e-6);

        root = scope.musicians;
        console.log(root);
        root.x0 = h / 2;
        root.y0 = 0;

        function toggleAll(d) {
          if (d.children) {
            d.children.forEach(toggleAll);
            toggle(d);
          }
        }

        function update(source) {
          var duration = d3.event && d3.event.altKey ? 5000 : 500;

          // Compute the new tree layout.
          var nodes = tree.nodes(root).reverse();

          // Normalize for fixed-depth.
          nodes.forEach(function(d) { d.y = d.depth * 180; });

          // Update the nodes…
          var node = vis.selectAll("g.node")
              .data(nodes, function(d) { return d.id || (d.id = ++i); });

          // Enter any new nodes at the parent's previous position.
          var nodeEnter = node.enter().append("svg:g")
              .attr("class", "node")
              .attr("transform", function(d) { return "translate(" + source.y0 + "," + source.x0 + ")"; })
              .on("click", function(d) { toggle(d); update(d); });

          nodeEnter.append("svg:circle")
              .attr("r", 1e-6)
              .style("fill", function(d) { return d._children ? "lightsteelblue" : "#fff"; });

          nodeEnter.append("svg:text")
              .attr("x", function(d) { return d.children || d._children ? -10 : 10; })
              .attr("dy", ".35em")
              .attr("text-anchor", function(d) { return d.children || d._children ? "end" : "start"; })
              .text(function(d) { return d.name; })
              .style("fill-opacity", 1e-6);

          // Transition nodes to their new position.
          var nodeUpdate = node.transition()
              .duration(duration)
              .attr("transform", function(d) { return "translate(" + d.y + "," + d.x + ")"; });

          nodeUpdate.select("circle")
              .attr("r", 4.5)
              .style("fill", function(d) { return d._children ? "lightsteelblue" : "#fff"; });

          nodeUpdate.select("text")
              .style("fill-opacity", 1);

          // Transition exiting nodes to the parent's new position.
          var nodeExit = node.exit().transition()
              .duration(duration)
              .attr("transform", function(d) { return "translate(" + source.y + "," + source.x + ")"; })
              .remove();

          nodeExit.select("circle")
              .attr("r", 1e-6);

          nodeExit.select("text")
              .style("fill-opacity", 1e-6);

          // Update the links…
          var link = vis.selectAll("path.link")
              .data(tree.links(nodes), function(d) { return d.target.id; });

          // Enter any new links at the parent's previous position.
          link.enter().insert("svg:path", "g")
              .attr("class", "link")
              .attr("d", function(d) {
                var o = {x: source.x0, y: source.y0};
                return diagonal({source: o, target: o});
              })
            .transition()
              .duration(duration)
              .attr("d", diagonal);

          // Transition links to their new position.
          link.transition()
              .duration(duration)
              .attr("d", diagonal);

          // Transition exiting nodes to the parent's new position.
          link.exit().transition()
              .duration(duration)
              .attr("d", function(d) {
                var o = {x: source.x, y: source.y};
                return diagonal({source: o, target: o});
              })
              .remove();

          // Stash the old positions for transition.
          nodes.forEach(function(d) {
            d.x0 = d.x;
            d.y0 = d.y;
          });
        }

        // Toggle children.
        function toggle(d) {
          if (d.children) {
            d._children = d.children;
            d.children = null;
          } else {
            d.children = d._children;
            d._children = null;
          }
        }

        // Initialize the display to show a few nodes.
        root.children.forEach(toggleAll);
        toggle(root.children[2]);
        toggle(root.children[2].children[1]);

        update(root);

        // Add the dot at every node
        function showTooltip(d) {
          tooltip.transition()
          .duration(300)
          .style("opacity", 1)
          .text("Info about " + d.name)
          .attr("href", d.url)
          .style("left", (d3.event.pageX ) + "px")
          .style("top", (d3.event.pageY) + "px");
        }

        function hideTooltip() {
          tooltip.transition()
          .duration(600)
          .style("opacity", 1e-6);
        }

        function preserveTooltip() {
          tooltip.transition()
          .duration(0)
          .style("opacity", 1);
        }

        vis.selectAll("g.node text")
        .on("mouseover", function(d){showTooltip(d);})
        .on("mouseout", hideTooltip);

        tooltip
        .on("mouseover", preserveTooltip)
        .on("mouseout", hideTooltip);

      }, 2000);
    };

    return {
      template: '',
      scope: {musicians: '=musicians'},
      link: link,
      restrict: 'EA'
    };

  }]);
