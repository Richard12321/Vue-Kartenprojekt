<template>
  <div>
    <label>Obstacletype: </label>
    <select v-model="selectedType">
      <option>Alle Anzeigen</option>
      <option v-for="i in types">{{ i }}</option>
    </select>
    <br />
    <br />
    <br />
    <button @click="drawObstacles" class="btn btn-primary" style="width: 175px; height: 50px;">Obstacles anzeigen</button>
    <br /> 
    <br />
    <br />
  </div>
  <GoogleMap api-key="" style="width: 750px; height: 750px" :center="center" :zoom="8.5" >
    <Polyline v-for="p in paths" :options="p" />
    <Marker v-for="m in markers" :options="m[0]">
      <InfoWindow :options="m[1]" />
    </Marker>
  </GoogleMap>
  <br />
</template>

<style>
@import "bootstrap";
</style>

<script>
import axios from "axios";
import { defineComponent } from "vue";
import { GoogleMap, Polyline, Marker, InfoWindow } from "vue3-google-map";

export default defineComponent({
  components: { GoogleMap, Polyline, Marker, InfoWindow },
  data() {
    return{
      allObstacles: [],
      paths: [],
      center: { lat: 47, lng: 11.5 },
      types: [],
      selectedType: "",
      markers: [],
    }
  },
  mounted() {
    this.getAllObstacles();
    this.getTypes();
  },
  methods: {
    getTypes(){
      axios.get("http://localhost:5000/allObstacleTypes").then((res) => {
        this.types = res.data
      });
    },
    getAllObstacles(){
      axios.get("http://localhost:5000/allObstacles").then((res) => {
        this.allObstacles = res.data.features
      });
    },
    getObstacles(){
      axios.get("http://localhost:5000/obstacles/" + this.selectedType).then((res) => {
        this.allObstacles = res.data
      });
    },
    drawObstacles(){
      const color = "#0000FF"
      this.allObstacles.forEach(element => {
        const pathCoordinates = [];
        element.geometry.coordinates.forEach(c =>{
          pathCoordinates.push({lat: c[1], lng: c[0]})
        });
        const newPath = {
          path: pathCoordinates,
          strokeColor: color,
          strokeOpacity: 1.0,
          strokeWeight: 2,
        };
        this.paths.push(newPath)
        const newMarker = {
          position: pathCoordinates[0]
        };
        const newInfowindow = {
          content: '<label style="color:black">' + element.properties.FLUGHINDERNIS + "</label>"
        }
        this.markers.push([newMarker, newInfowindow])
      });
    },
  },
  watch: {
    selectedType: function () {
      if(this.selectedType == "Alle Anzeigen"){
        this.getAllObstacles();
      } else {
        this.getObstacles();
      }
    },
  },
});

</script>