<script>
  import svelteLogo from "./assets/svelte.svg";
  import viteLogo from "/vite.svg";
  import Counter from "./lib/Counter.svelte";
  import NewComponent from "./lib/Bored.svelte";
  import Map from "./lib/Map.svelte";
  import Searchbar from "./lib/Searchbar.svelte";
</script>

<main>
  <h1>Goval</h1>
  <NewComponent onincrement={() => console.log("Count")} />
  <div class="search-bar">
    <Searchbar />
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
