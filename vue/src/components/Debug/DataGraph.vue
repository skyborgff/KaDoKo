<template>
  <div class="container-fluid col flex-grow-1 h-100">
    <div class="container-fluid row flex-grow-1 h-100" id="3d-graph"></div>
    <div style="position: absolute; top: 5px; left: 5px;">
      <button id="animationToggle" style="margin: 8px; height: 30px; width: 150px;">
        Pause Animation
      </button>
      <button id="animationRestart" style="margin: 8px; height: 30px; width: 150px;">
        Animate More
      </button>
    </div>
  </div>
</template>

<script>
  /* eslint-disable */
  // https://github.com/vasturiano/3d-force-graph
  // https://github.com/vasturiano/force-graph
  // https://github.com/vasturiano/d3-force-registry

  import axios from 'axios';
  import ForceGraph3D from '3d-force-graph';
  import ForceGraph from 'force-graph';
  import * as d3 from 'd3-force-3d';  // eslint-disable-line no-unused-vars
  import * as d3Sampled from 'd3-force-sampled';  // eslint-disable-line no-unused-vars
  import * as THREE from 'three';  // eslint-disable-line no-unused-vars
  import * as dat from 'dat.gui';
  import Anime from "../Settings/Anime";

  export default {
    name: "DataGraph",
    data: function () {
      return {
        nodes: [],
        links: [],
        nodesById: [],
        ClassLinksCount: {},
        ClassCount: {},
        graph_data: {},
        Class_dict: {
          "Anime": {
            "class_name": "Anime",
            "color": "Yellow",
            "radius": 3,
            "radius3": 20,
            "distance": 10000,
            "s_radial": 1,
            "s_radial3": 0.3
          },
          "AnimeList": {
            "class_name": "AnimeList",
            "color": "Green",
            "radius": 5,
            "radius3": 5,
            "distance": 500,
            "s_radial": 0.05,
            "s_radial3": 0.1
          },
          "AnimeLists": {
            "class_name": "AnimeLists",
            "color": "Green",
            "radius": 20,
            "radius3": 10,
            "distance": 0,
            "s_radial": 0.05,
            "s_radial3": 0.1
          },
          "Tag": {"class_name": "Tag", "color": "Cyan", "radius": 0.5, "radius3": 1, "distance": 0, "s_radial": 0.01},
          "Episode": {"class_name": "Episode", "color": "Cyan", "radius": 0.5, "radius3": 1, "distance": 0, "s_radial": 0},
          "Episodes": {"class_name": "Episodes", "color": "Cyan", "radius": 0.5, "radius3": 1, "distance": 0, "s_radial": 10},
          "Other": {
            "class_name": "Other",
            "color": "Cyan",
            "radius": 0.5,
            "radius3": 1,
            "distance": 15000,
            "s_radial": 0.1,
            "s_radial3": 0.001
          }
        },
        graph_type: this.$route.params.graph_type,
      }
    },
    mounted: function () {
      this.get_graph();
    },
    methods: {
      get_graph() {
        const path = 'http://localhost:8283/force/force.json';
        axios.get(path).then((res) => this.display_graph(res));
      },
      display_graph(res) {
        const start = new Date()
        this.graph_data = res.data;
        this.nodes = this.graph_data['nodes'];
        this.links = this.graph_data['links'];

        const links = this.links.map(r => {
          return {
            source: r['source'].toString(),
            target: r['target'].toString()
          }
        });
        window.console.log(links.length + " links loaded " + (new Date() - start) + " ms.")
        const ids = new Set();
        links.forEach(l => {
          ids.add(l.source);
          ids.add(l.target);
        });
        var rootId = null;

        var ClassLinksCount = {};
        for (var link_id in this.links) {
          var link = this.links[link_id]
          ClassLinksCount[link.source] = (ClassLinksCount[link.source] || 0) + 1;
          ClassLinksCount[link.target] = (ClassLinksCount[link.target] || 0) + 1;
        }
        this.ClassLinksCount = ClassLinksCount;

        var ClassCount = {};
        for (var node_id in this.nodes) {
          var node = this.nodes[node_id]
          var class_name = this.ClassData(node, "class_name")
          ClassCount[class_name] = (ClassCount[class_name] || 0) + 1;
        }
        this.ClassCount = ClassCount;

        var anime_diameter = this.Class_dict["Anime"]["radius"]*2
        var minimum_anime_perimeter = this.ClassCount["Anime"]*anime_diameter*5
        this.Class_dict["Anime"]["distance"] = (minimum_anime_perimeter*2)/2/3.14

        var other_diameter = this.Class_dict["Other"]["radius"]*2
        var minimum_other_perimeter = this.ClassCount["Other"]*other_diameter*10
        this.Class_dict["Other"]["distance"] = (minimum_other_perimeter*2)/2/3.14
        this.Class_dict["Tag"]["distance"] = this.Class_dict["Other"]["distance"]
        this.Class_dict["Episodes"]["distance"] = this.Class_dict["Other"]["distance"]
        this.Class_dict["Episode"]["distance"] = this.Class_dict["Episodes"]["distance"]+20


        var animeIndexer = 0
        var listIndexer = 0
        var otherIndexer = 0
        var episodeIndexer = 0
        var episodesIndexer = 0
        const nodes = Array.from(this.nodes).map(node => {
          var angle = Math.random()*Math.PI*2 - Math.PI/2
          var x = Math.cos(angle) * this.ClassData(node, "distance")
          var y = Math.sin(angle) * this.ClassData(node, "distance")
          var fixedx = null
          var fixedy = null
          if (this.ClassLabel(node)[0] === "Anime"){
            angle = Math.PI*2/ClassCount["Anime"]*animeIndexer - Math.PI/2
            animeIndexer+=1
            fixedx = Math.cos(angle) * this.ClassData(node, "distance")
            fixedy = Math.sin(angle) * this.ClassData(node, "distance")
          }
          else if (this.ClassLabel(node)[0] === "AnimeList"){
            angle = Math.PI*2/ClassCount["AnimeList"]*listIndexer - Math.PI/2
            listIndexer+=1
            fixedx = Math.cos(angle) * this.ClassData(node, "distance")
            fixedy = Math.sin(angle) * this.ClassData(node, "distance")
          }
          else if (this.ClassLabel(node)[0] === "AnimeLists"){
            fixedx = 0
            fixedy = 0
          }
          else if (this.ClassData(node, "class_name") === "Other"){
            angle = Math.PI*2/ClassCount["Other"]*otherIndexer - Math.PI/2
            otherIndexer+=1
            x = Math.cos(angle) * this.ClassData(node, "distance")
            y = Math.sin(angle) * this.ClassData(node, "distance")
          }
          else if (this.ClassData(node, "class_name") === "Episode"){
            angle = Math.PI*2/ClassCount["Episode"]*episodeIndexer - Math.PI/2
            episodeIndexer+=1
            x = Math.cos(angle) * this.ClassData(node, "distance")
            y = Math.sin(angle) * this.ClassData(node, "distance")
          }
          else if (this.ClassData(node, "class_name") === "Episodes"){
            angle = Math.PI*2/ClassCount["Episodes"]*episodesIndexer - Math.PI/2
            episodesIndexer+=1
            x = Math.cos(angle) * this.ClassData(node, "distance")
            y = Math.sin(angle) * this.ClassData(node, "distance")
          }
          return {
            id: node["id"].toString(),
            data_class: this.ClassLabel(node)[0],
            class_name: this.ClassData(node, "class_name"),
            label: this.ClassLabel(node)[1],
            radius: this.ClassData(node, "radius"),
            radius3: this.ClassData(node, "radius3"),
            area: 3.14 * this.ClassData(node, "radius") ** 2,
            volume: 4 / 3 * 3.14 * this.ClassData(node, "radius3") ** 3,
            distance: this.ClassData(node, "distance"),
            collapsed: this.ClassLabel(node)[0] !== "AnimeLists",
            // collapsed: false,
            childLinks: [],
            x: x,
            y: y,
            fx: fixedx,
            fy: fixedy,
            fz: 0,
            vx: 0,
            vy: 0,
            vz: 0,
          }
        });
        for (var node_id in this.nodes) {
          // if (this.ClassLabel(this.nodes[node_id])[0] === "AnimeList"){
          //   rootId.push(this.nodes[node_id].id)
          // }
          if (this.ClassLabel(this.nodes[node_id])[0] === "AnimeLists") {
            rootId = this.nodes[node_id].id
          }
          // if (this.ClassLabel(this.nodes[node_id])[0] === "AnimeList") {
          //   rootId.push(this.nodes[node_id].id)
          // }
        }

        const gData = {nodes: nodes, links: links};

        // link parent/children
        var nodesById = Object.fromEntries(gData.nodes.map(node => [node.id, node]));
        gData.links.forEach(link => {
          nodesById[link.source].childLinks.push(link);
        });
        this.nodesById = nodesById;



        const getPrunedTree = () => {
          const visibleNodes = [];
          const visibleLinks = [];

          (function traverseTree(node = nodesById[rootId]) {
            visibleNodes.push(node);
            if (node.collapsed) return;
            visibleLinks.push(...node.childLinks);
            node.childLinks
              .map(link => ((typeof link.target) === 'object') ? link.target : nodesById[link.target]) // get child node
              .forEach(traverseTree);
          })(); // IIFE


          return {nodes: visibleNodes, links: visibleLinks};
        };

        var elem = document.getElementById('3d-graph')

        function toggle_visibility(visible) {
          console.log(visible);
          gData.nodes.forEach(nodeindex => {
            var node = nodesById[nodeindex.id];
            if (node.collapsed === visible) {
              if (node.data_class !== "AnimeLists") {
                node.collapsed = !visible;
                // var angle = Math.random()*Math.PI*2
                // node.x = Math.cos(angle) * node.distance;
                // node.y = Math.sin(angle) * node.distance;
                // node.z = (Math.random() - 0.5) * node.distance * 2;
                // node.vx = 0;
                // node.vy = 0;
                // node.vz = 0;
              }
            }
          });
          Graph.graphData(getPrunedTree())
          Graph.zoomToFit(0)
          Graph.cooldownTime(50000)
          if (!visible){Graph.cooldownTime(1000)}

        }

        var toggle = {
          ShowAll: function () {
            toggle_visibility(true)
          },
          HideAll: function () {
            toggle_visibility(false)
          }
        };
        const gui = new dat.GUI();
        gui.add(toggle, 'ShowAll');
        gui.add(toggle, 'HideAll');

        var Graph = null;
        var rel_size = 10; // eslint-disable-line no-unused-vars
        window.devicePixelRatio = 1;


        if (this.graph_type === "3D") {
          rel_size = 10; // eslint-disable-line no-unused-vars
          Graph = ForceGraph3D()(elem).graphData(getPrunedTree())
            .d3AlphaDecay(0)
            .d3VelocityDecay(0.3)
            // .warmupTicks(600)
            .warmupTicks(0)
            .cooldownTime(100000)
            .nodeVal('volume')
            // .nodeResolution(1)
            // .linkDirectionalArrowResolution(3)
            .linkDirectionalArrowLength(20)
            .d3Force("radial", d3.forceRadial().radius(d => this.ClassData(d, "distance") / 2).strength(d => this.ClassData(d, "s_radial3")))
            .d3Force('link', d3.forceLink().strength(link => this.LinkStatus(link)[0]).id(d => d.id).distance(link => this.LinkStatus(link)[1]))
            .d3Force('center', d3.forceCenter().strength(0.02))
            .d3Force('collision', d3.forceCollide(node => node.radius3 * rel_size).strength(1))
            // .d3Force('radial', null)
            // .d3Force('link', null)
            // .d3Force('center', null)
            // .d3Force('collision', null)
            .d3Force('charge', null)


        } else {
          Graph = ForceGraph()(elem).graphData(getPrunedTree())
            .zoom(0.5, 0)
            .d3AlphaDecay(0)
            .d3VelocityDecay(0.3)
            // .warmupTicks(50)
            .cooldownTime(1000)
            .nodeVal('area')
            .linkDirectionalArrowLength(6)
            .d3Force('collision', d3.forceCollide(node => node.radius * rel_size).strength(10))
            .d3Force('center', d3.forceCenter(0, 0).strength(0.02))
            .d3Force("charge", d3Sampled.forceManyBodySampled().strength(-0.001).distanceMax(100))
            .d3Force('link', d3.forceLink().strength(link => this.LinkStatus(link)[0]).id(d => d.id).distance(link => this.LinkStatus(link)[1]))
            .d3Force("radial", d3.forceRadial().radius(d => this.ClassData(d, "distance")).strength(d => this.ClassData(d, "s_radial")))
          // .d3Force('collision', null)
          .d3Force('center', null)
          .d3Force('charge', null)
          // .d3Force('link', null)
          .d3Force('radial', null)
        }

        Graph
          .linkDirectionalArrowRelPos(1)
          .nodeAutoColorBy('data_class')
          .nodeLabel(node => `${node.data_class}\n ${node.label}`)
          .onNodeHover(node => elem.style.cursor = node ? 'pointer' : null)
          .onEngineStop(() => Graph.zoomToFit(400))
          .onNodeClick(node => {
            if (node.childLinks.length) {
              node.collapsed = !node.collapsed;
              Graph.cooldownTime(1000)
              Graph.graphData(getPrunedTree());
              Graph.d3ReheatSimulation()
            }
          })
          .onNodeDragEnd(node => {
            node.fx = node.x;
            node.fy = node.y;
            node.fz = node.z;
            Graph.cooldownTime(1000)
            Graph.d3ReheatSimulation()
          })
          .onNodeRightClick(node => {
            // Should show info
            delete node.fx;
            delete node.fy;
            delete node.fz;
            Graph.cooldownTime(1000)
            Graph.d3ReheatSimulation()
          })
        ;
            var height = elem.offsetHeight, width = elem.offsetWidth;
            Graph.width(width).height(height);

        let isAnimationActive = true;
        document.getElementById('animationToggle').addEventListener('click', event => {
          isAnimationActive ? Graph.pauseAnimation() : Graph.resumeAnimation();

          isAnimationActive = !isAnimationActive;
          event.target.innerHTML = `${(isAnimationActive ? 'Pause' : 'Resume')} Animation`;
        });
        document.getElementById('animationRestart').addEventListener('click', function () {
          Graph.d3ReheatSimulation()
        });
        window.addEventListener('resize', resize);
        function resize() {
            elem = document.getElementById('3d-graph')
            var height = elem.offsetHeight, width = elem.offsetWidth;
            Graph.width(width).height(height);

        }
      },
      LinkStatus(link) {
        var source = link.source;
        var target = link.target;

        var source_node = this.nodesById[source.id];
        var target_node = this.nodesById[target.id];

        var source_class = source_node.class_name;// eslint-disable-line no-unused-vars
        var target_class = target_node.class_name;// eslint-disable-line no-unused-vars

        var source_count = this.ClassLinksCount[source.id];// eslint-disable-line no-unused-vars
        var target_count = this.ClassLinksCount[target.id];// eslint-disable-line no-unused-vars

        var s_base = 0;
        var d_base = 1000;

        s_base = s_base / target_count;

        var allowed_class1 = ["AnimeList", "AnimeLists"]// eslint-disable-line no-unused-vars
        var allowed_class2 = ["Episodes"]// eslint-disable-line no-unused-vars
        var allowed_class3 = ["Anime"]// eslint-disable-line no-unused-vars
        var allowed_class4 = ["Tag"]// eslint-disable-line no-unused-vars

        // if (allowed_class1.includes(source_class)) {
        //   d_base = 10000
        //   s_base = 0
        // }

        // if (allowed_class4.includes(target_class)) {
        //   d_base = 2000
        //   s_base = 0.001
        // }
        // if (source_class === "Anime" && target_class !== "Tag") {
        //   d_base = 100
        //   s_base = 0.01
        // }
        // if (target_class === "Anime") {
        //   d_base = 11000
        //   s_base = 0.01
        // }
        if (source_class === "Episodes") {
          d_base = target_count*2
          s_base = 0.01/target_count
        }
        if (source_class === "Anime") {
          d_base = 10000
          s_base = 0.1/source_count
        }
        if (source_class === "Other") {
          d_base = 50
          s_base = 0.1
        }
        // if (target_class === "Episodes") {
        //   d_base = 300
        //   s_base = 0.01
        // }

        return [s_base, d_base]
      },
      ClassLabel(d) {
        var classes = "";
        var label = "";
        if ("data_class" in d) {
          classes = d.data_class;
          label = d.label
        } else {
          if ("data" in d) {
            if ("py/object" in d.data) {
              classes = d.data["py/object"]
            }
            if ("py/type" in d.data) {
              classes = d.data["py/type"]
            }
          }
        }
        return [classes, label];
      },
      ClassData(d, data) {
        var processed_data = this.Class_dict[d.data_class] ? this.Class_dict[d.data_class][data] : this.Class_dict["Other"][data]
        return processed_data
      },
    },

  }


</script>

<style>
  .dg.a {
    margin-top: 50px !important;
  }
</style>