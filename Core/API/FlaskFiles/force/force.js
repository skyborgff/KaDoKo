// This is adapted from https://bl.ocks.org/mbostock/2675ff61ea5e063ede2b5d63c08020c7
// https://bl.ocks.org/jodyphelan/5dc989637045a0f48418101423378fbd
// https://bl.ocks.org/steveharoz/8c3e2524079a8c440df60c1ab72b5d03
// https://observablehq.com/collection/@d3/d3-force


// d3.selectAll("circle").filter(function(d, i) {return d.data_class == "AnimeList"})

// Replace with
// https://blog.scottlogic.com/2020/05/01/rendering-one-million-points-with-d3.html
// https://d3fc.io/

var Class_dict = {
  "Anime": {"color": "Yellow", "radius": 6},
  "AnimeList": {"color": "Green", "radius": 9},
  "Other": {"color": "Cyan", "radius": 3}
};

function ClassRadius(d) {
  return Class_dict[d.data_class] ? Class_dict[d.data_class]["radius"] : Class_dict["Other"]["radius"]
};

function ClassColor(d) {
  return Class_dict[d.data_class] ? Class_dict[d.data_class]["color"] : Class_dict["Other"]["color"]
};

function ClassLabel(d) {
  var classes = ""
  var label = ""
  var info = ""
  if ("data_class" in d) {
    classes = d.data_class
    label = d.label
  }
  else{if ("data" in d) {
    if ("py/object" in d.data) {
      classes = d.data["py/object"]
    }
    if ("py/type" in d.data) {
      classes = d.data["py/type"]
    }
  }}
  return [classes, label, info];
};

var height = window.innerHeight;
var width = window.innerWidth;

const zoom = d3.zoom().on("zoom", () => {
  svg.attr("transform", d3.event.transform)
});

var svg = d3.select("svg")
  .attr("width", width)
  .attr("height", height)
  .call(zoom)
  .append("g")



var simulation = d3.forceSimulation()
  .force("center", d3.forceCenter(width / 2, height / 2))
  .force("x", d3.forceX(width / 2).strength(d => (ClassRadius(d)) ** 2))
  .force("y", d3.forceY(height / 2).strength(d => (ClassRadius(d)) ** 2))
  .force("charge", d3.forceManyBody().strength(-10000))
  //.force("charge", d3.forceManyBody().strength(d => -((ClassRadius(d)/3)**5)*500))
  .force("link", d3.forceLink().strength(1).id(d => d.id))
  //.force("link", d3.forceLink().strength(d => (4-ClassRadius(d)/3)**3).id(d => d.id))
  .force("collide", d3.forceCollide().radius(d => ClassRadius(d)).strength(1))
  .force("radial", d3.forceRadial().radius(d => ((1 - ((ClassRadius(d) / 3) - 2)) ** 2) * 500 + 50).strength(30).x(width / 2).y(height / 2))
  .alphaTarget(0.0)
  .alphaDecay(0.09)

d3.json("force/force.json", json_packer);

function json_packer(error, graph) {
  if (error) throw error;

  var graph_nodes = graph.nodes
  var graph_links = graph.links

  var links = svg.append("g")
    .attr("class", "links")
    .selectAll("line")
    .data(graph_links)
    .enter().append("line")
    .attr("stroke-width", 1)
    .attr('marker-end', 'url(#arrowhead)');


  var nodes = svg.append("g")
      .attr("class", "nodes")
    .selectAll("circle")
    .data(graph_nodes)
    .enter().append('g')
    .attr("class", "node")
    .classed("fixed", d => d.fx !== undefined)
    .call(d3.drag()
      .on("start", dragstarted)
      .on("drag", dragged)
      .on("end", dragended)
    )
    .on("click", click);


  var circles = nodes.append("circle")
    .attr("r", function (d) {
      return ClassRadius(d);
    })
    .style("fill", d => ClassColor(d))

  var classes = nodes.append("text")
    .text(function (d) {
      return ClassLabel(d)[0];
    })
    .style("font-size", "2px")
    .style("text-anchor", "middle")
    .attr('x', 0)
    .attr('y', 0);
  var labels = nodes.append("text")
    .text(function (d) {
      return ClassLabel(d)[1];
    })
    .style("font-size", "2px")
    .style("text-anchor", "middle")
    .attr('x', 0)
    .attr('y', 2);

  var arrow = svg.append('defs').append('marker')
    .attr('id', 'arrowhead')
    .attr('viewBox', '-0 -5 10 10')
    .attr('refX', 20)
    .attr('refY', 0)
    .attr('orient', 'auto')
    .attr('markerWidth', 20)
    .attr('markerHeight', 10)
    .attr('xoverflow', 'visible')
    .append('svg:path')
    .attr('d', 'M 0,-5 L 10 ,0 L 0,5')
    .attr('fill', '#999')
    .style('stroke', 'none');


  simulation
    .nodes(graph.nodes)
    .on("tick", tick);

  simulation.force("link")
    .links(graph.links);

  function render() {

  }

  function tick() {
    links
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
      })
      .attr("refX", d => ClassRadius(d.target) * 2 + 10);

    nodes
      .attr("transform", function (d) {
        return "translate(" + d.x + "," + d.y + ")";
      })

  }

}


function dragstarted(d) {
  d3.select(this).classed("fixed", true);
  if (!d3.event.active) simulation.alphaTarget(0.01).restart();
  d.fx = d.x;
  d.fy = d.y;
}

function dragged(d) {
  d.fx = d3.event.x;
  d.fy = d3.event.y;
}

function dragended(d) {
  if (!d3.event.active) simulation.alphaTarget(0);
  // = Null to make it go to the correct place
  d.fx = d.x;
  d.fy = d.y;
}

function click(d) {
  delete d.fx;
  delete d.fy;
  d3.select(this).classed("fixed", false);
  simulation.alpha = 0.01;
  simulation.restart();
}