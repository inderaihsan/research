<script>
  import NewComponent from "./component/Bored.svelte";
  import Map from "./component/Map.svelte";
  import Searchbar from "./component/Searchbar.svelte";

  import { onMount } from 'svelte';

  let posyanduData;

  onMount(async () => {
    const res = await fetch('http://127.0.0.1:8000/spatial/get-posyandu-data', {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      },
    });
    posyanduData = await res.json();
  });

  






async function getwadmkc(wadmkc) {
  const query = new URLSearchParams({ wadmkc });

  const response = await fetch(`http://127.0.0.1:8000/spatialanalysis/get-wadmkc`, {
    method: "GET",
    headers: {
      "Content-Type": "application/json",
    }
  });

  if (!response.ok) throw new Error("Failed to fetch wadmkc...");
  return await response.json();
}
    
</script>

<main>
  <h1>Goval</h1>
  <NewComponent onincrement={() => console.log("Count")} />
  <div class="search-bar">
    <Searchbar onsearch = { ()=> getwadmkc() } />
  </div>
  <div class="map">
    <Map height="650px"></Map>
  </div>
</main>

<style>
  .map {
    height: 90em;
    width: 80em;
    padding: 1.5em;
  }
</style>
