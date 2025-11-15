<script>
  import { onMount } from "svelte";
  import Map from "./component/Map.svelte";
  import Bored from "./component/Bored.svelte";

  let renderData = null;
  let loading = true;

  onMount(async () => {
    try {
      const res = await fetch(
        "http://127.0.0.1:8000/spatial/get-posyandu-data"
      );
      const data = await res.json();

      renderData = data.data; // store the GeoJSON
      console.log(renderData);
    } catch (e) {
      console.error("Failed to load geojson", e);
    } finally {
      loading = false;
    }
  });
</script>

<main>
  {#if loading}
    <p>Loading map data...</p>
  {:else}
    <!-- <Map {renderData} /> -->
    <div class="map">
      <Map height="650px" {renderData}></Map>
    </div>
  {/if}
</main>

<style>
  .map {
    height: 90em;
    width: 80em;
    padding: 1.5em;
  }
</style>
