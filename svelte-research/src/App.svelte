<script>
  import svelteLogo from "./assets/svelte.svg";
  import viteLogo from "/vite.svg";
  import Counter from "./component/Counter.svelte";
  import NewComponent from "./component/Bored.svelte";
  import Map from "./component/Map.svelte";
  import Searchbar from "./component/Searchbar.svelte";
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
