<template>
  <div class="row flex-grow-1 h-100">
    <div class="col-3 h-100">
    <json-viewer :value="nodeRaw" theme="jv-light" :expand-depth=6 copyable h-100></json-viewer>
    </div>
    <div class="col h-100">
      <div  id="3d-graph" class="h-100"></div>
    <div style="position: absolute; top: 5px; left: 5px;">
      <button id="animationToggle" style="margin: 8px; height: 30px; width: 150px;">
        Pause Animation
      </button>
      <button id="animationRestart" style="margin: 8px; height: 30px; width: 150px;">
        Animate More
      </button>
    </div></div>

  </div>
</template>

<script>
  /* eslint-disable */
  // https://github.com/vasturiano/3d-force-graph
  // https://github.com/vasturiano/force-graph
  // https://github.com/vasturiano/d3-force-registry

  // https://github.com/vasturiano/3d-force-graph/issues/408

  import axios from 'axios';
  import ForceGraph3D from '3d-force-graph';
  import ForceGraph from 'force-graph';
  import * as d3 from 'd3-force-3d';  // eslint-disable-line no-unused-vars
  import * as d3Sampled from 'd3-force-sampled';  // eslint-disable-line no-unused-vars
  import * as THREE from 'three';  // eslint-disable-line no-unused-vars
  import * as dat from 'dat.gui';
  import Anime from "../Settings/Anime";
  import SpriteText from "three-spritetext"

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
        nodeRaw: {'null': 'null'}
      }
    },
    filters: {
    pretty: function(value) {
      return JSON.stringify(JSON.parse(value), null, 2);
    }},
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

        var deleted_nodes = []
        var nodes = Array()
        this.nodes.forEach(node => {
          if (node.data_class !== "AnimeList" && node.data_class !== "AnimeLists"){
          nodes.push({
            id: node["id"].toString(),
            data_class: node.data_class ? node.data_class : "NO CLASS ERROR",
            label: node.label ? node.label : "",
            raw: node,
          })}
          else{
            deleted_nodes.push(node.id)
          }
        });

        var links = Array()
        this.links.forEach(r => {
          var source = r['source'].toString()
          var target = r['target'].toString()
          if (!deleted_nodes.includes(source) && !deleted_nodes.includes(target)){
          links.push( {
            source: source,
            target: target
          })}});

        window.console.log(this.links.length + " links and " + this.nodes.length + " nodes loaded " + (new Date() - start) + " ms.")


        const gData = {nodes: nodes, links: links};

        var nodesById = Object.fromEntries(this.nodes.map(node => [node.id, node]));

        window.console.log("Loading Graph")

        var elem = document.getElementById('3d-graph')
        var radius = 0.9
        var volume = 4/3*Math.PI*radius**3
        var Graph = ForceGraph3D({ rendererConfig: { antialias: true, alpha: true, powerPreference: "high-performance"} })(elem)
          .graphData(gData)
          // .jsonUrl('http://localhost:8283/force/force.json')
          .nodeLabel(node => `${node.data_class}\n ${node.label}`)
          .nodeAutoColorBy('data_class')
          .nodeVal(volume)
          // .nodeResolution(1)
          .linkDirectionalArrowResolution(3)
          .linkAutoColorBy(link => nodesById[link.target].data_class)
          .linkDirectionalArrowLength(radius*5)
          .linkDirectionalArrowRelPos(1)
          .numDimensions(3)
          .d3Force("collision", d3.forceCollide(radius).strength(100))
          // .d3Force("magnet", d3.forceManyBody().strength(10).distanceMax(radius*5))
          // .d3Force("charge", d3.forceManyBody().strength(-1000).distanceMax(radius*100))
          // .d3Force("charge2", d3.forceManyBody().strength(-10).distanceMin(radius*100))
          // .d3Force('radial', null)
          // .d3Force('link', null)
          // .d3Force('center', null)
          // .d3Force('collision', null)
          // .d3Force('charge', null)
          .d3AlphaDecay(0)
          .d3VelocityDecay(0.2)
          // .dagMode("radialout")
          // .dagLevelDistance(radius*500)
          .backgroundColor("#343a40")
          .warmupTicks(20)
          .cooldownTicks(0)
          .onNodeHover(node => elem.style.cursor = node ? 'pointer' : null)
          .onEngineStop(() => {Graph.zoomToFit(400); Graph.onEngineStop(()=>{})})
          .onNodeClick(node => {
              this.nodeRaw = node.raw
          })
          // .onNodeDragEnd(node => {
          // })
          // .onNodeRightClick(node => {
          // })
          .nodeThreeObjectExtend(true)
          .nodeThreeObject(
          node => {
            const sprite = new SpriteText(node.data_class);
            sprite.color = '#BFBFBF';
            sprite.textHeight = 5;
            sprite.fontSize = 30;
            return sprite;
			}
		)
        ;
        window.console.log("Graph loaded in " + (new Date() - start) + " ms.")
        var height = elem.offsetHeight, width = elem.offsetWidth;
        Graph.width(width).height(height-60);

        document.getElementById('animationRestart').addEventListener('click', function () {
          Graph.cooldownTicks(100).d3ReheatSimulation()
        });
                document.getElementById('animationToggle').addEventListener('click', function () {
          Graph.cooldownTicks(0).d3ReheatSimulation()
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
  .jv-container{background: var(--gray-dark) !important;}
  .jv-key{color: var(--white) !important;}
  .jv-node:after{color: var(--white) !important;}

</style>