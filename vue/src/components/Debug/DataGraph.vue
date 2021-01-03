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
        NodeLinksCount: {},
        ClassCount: {},
        graph_data: {},
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

        const links = this.links.map(r => {return {
            source: r['source'].toString(),
            target: r['target'].toString()
          }});

        window.console.log(this.links.length + " links and " + this.nodes.length + " nodes loaded " + (new Date() - start) + " ms.")

        const nodes = Array.from(this.nodes).map(node => {
          return {
            id: node["id"].toString(),
            data_class: node.data_class,
            label: node.label,
          }
        });

        const gData = {nodes: nodes, links: links};

        var nodesById = Object.fromEntries(gData.nodes.map(node => [node.id, node]));


        var elem = document.getElementById('3d-graph')
        var radius = 0.9
        var volume = 4/3*Math.PI*radius**3
        var Graph = ForceGraph3D()(elem)
          .graphData(gData)
          .nodeLabel(node => `${node.data_class}\n ${node.label}`)
          .nodeAutoColorBy('data_class')
          .nodeVal(volume)
          .linkAutoColorBy(link => nodesById[link.source].data_class)
          .linkDirectionalArrowLength(radius*10)
          .linkDirectionalArrowRelPos(1)
          // .d3Force("collision", d3.forceCollide(radius).strength(100))
          // .d3Force("magnet", d3.forceManyBody().strength(10).distanceMax(radius*5))
          // .d3Force("charge", d3.forceManyBody().strength(-100).distanceMin(radius*5))
          .d3AlphaDecay(0)
          .d3VelocityDecay(0.2)
          .dagMode(null)
          .dagLevelDistance(radius*500)
          .warmupTicks(0)
          .cooldownTicks(10000)
          .onNodeHover(node => elem.style.cursor = node ? 'pointer' : null)
          .onEngineStop(() => Graph.zoomToFit(400))
          .onNodeClick(node => {
          })
          .onNodeDragEnd(node => {
          })
          .onNodeRightClick(node => {
          })
        ;

        var height = elem.offsetHeight, width = elem.offsetWidth;
        Graph.width(width).height(height);

        document.getElementById('animationRestart').addEventListener('click', function () {
          Graph.cooldownTicks(100).d3ReheatSimulation()
        });

        window.addEventListener('resize', resize);
        function resize() {
            elem = document.getElementById('3d-graph')
            var height = elem.offsetHeight, width = elem.offsetWidth;
            Graph.width(width).height(height);

        }
      },
    },

  }


</script>

<style>
  .dg.a {
    margin-top: 50px !important;
  }
</style>