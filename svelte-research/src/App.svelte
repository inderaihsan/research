<script>
  import { onMount } from "svelte";
  import Map from "./component/Map.svelte";
  import Barchart from "./component/Barchart.svelte"; 
  import LineChart from "./component/LineChart.svelte";
  let heatmapMode = false;

  let renderData = null;
  let loading = true;
  let wadmkcList = [];
  let wadmkdList = [];
  let selectedWadmkc = "";
  let selectedWadmkd = "";
  let loadingWadmkd = false;
  let searching = false;
  let chartLabels = [];
  let chartValue = [];

  onMount(async () => {
    try {
      // Load initial posyandu data
      const posyanduData = await fetch(
        "http://127.0.0.1:8000/spatial/get-posyandu-data"
      );
      const data = await posyanduData.json();
      renderData = data.data;
      chartLabels = data.chart_data.label;
      chartValue = data.chart_data.values;

      // Load wadmkc list for dropdown
      const wadmkcResponse = await fetch(
        "http://127.0.0.1:8000/spatial/get-wadmkc"
      );
      wadmkcList = await wadmkcResponse.json();
      wadmkcList = wadmkcList.data;

      console.log("Initial data loaded", { renderData, wadmkcList });
    } catch (e) {
      console.error("Failed to load initial data", e);
    } finally {
      loading = false;
    }
  });

  // When wadmkc is selected, fetch wadmkd options
  async function handleWadmkcChange() {
    if (!selectedWadmkc) {
      wadmkdList = [];
      selectedWadmkd = "";
      return;
    }

    try {
      loadingWadmkd = true;
      selectedWadmkd = ""; // Reset wadmkd selection

      const wadmkdResponse = await fetch(
        `http://127.0.0.1:8000/spatial/get-wadmkd?wadmkc=${encodeURIComponent(selectedWadmkc)}`
      );
      wadmkdList = await wadmkdResponse.json();
      wadmkdList = wadmkdList.data;

      console.log("Wadmkd data loaded", wadmkdList);
    } catch (e) {
      console.error("Failed to load wadmkd", e);
      wadmkdList = [];
    } finally {
      loadingWadmkd = false;
    }
  }

  // Search with selected parameters
  async function handleSearch() {
    if (!selectedWadmkc) {
      alert("Please select at least kecamatan");
      return;
    }

    try {
      const response = await fetch(
        `http://127.0.0.1:8000/spatial/get-posyandu-data-query?wadmkc=${encodeURIComponent(selectedWadmkc)}&wadmkd=${encodeURIComponent(selectedWadmkd)}`
      );
      const data = await response.json();

      // CRITICAL: Create a NEW object, don't mutate
      renderData = { ...data.data }; // or just: renderData = data.data;
      chartLabels = data.chart_data.label;
      chartValue = data.chart_data.values;
    } catch (e) {
      console.error("Failed to search", e);
    }
  }

  function setHeatmapMode(mode) {
    heatmapMode = mode;
    console.log("Heatmap mode set to:", heatmapMode);
  }

  // Reset to show all data
  async function handleReset() {
    try {
      const response = await fetch(
        "http://127.0.0.1:8000/spatial/get-posyandu-data"
      );
      const data = await response.json();
      chartLabels = data.chart_data.label;
      chartValue = data.chart_data.values;

      // CRITICAL: Create a NEW object
      renderData = { ...data.data }; // or just: renderData = data.data;
    } catch (e) {
      console.error("Failed to reset", e);
    }
  }
</script>

<main>
  {#if loading}
    <p>Loading map data...</p>
  {:else}
    <div class="filter-container">
      <div class="dropdown-group">
        <label for="wadmkc">Kecamatan:</label>
        <select
          id="wadmkc"
          bind:value={selectedWadmkc}
          onchange={handleWadmkcChange}
          class="dropdown"
        >
          <option value="">-- Select Kecamatan --</option>
          {#each wadmkcList as wadmkc}
            <option value={wadmkc.value || wadmkc}>
              {wadmkc.label || wadmkc}
            </option>
          {/each}
        </select>
      </div>

      <div class="dropdown-group">
        <label for="wadmkd">Kelurahan:</label>
        <select
          id="wadmkd"
          bind:value={selectedWadmkd}
          class="dropdown"
          disabled={!selectedWadmkc || loadingWadmkd}
        >
          <option value="">
            {loadingWadmkd ? "Loading..." : "-- Select Kelurahan --"}
          </option>
          {#each wadmkdList as wadmkd}
            <option value={wadmkd.value || wadmkd}>
              {wadmkd.label || wadmkd}
            </option>
          {/each}
        </select>
      </div>

      <div class="button-group">
        <button
          onclick={handleSearch}
          disabled={!selectedWadmkc || searching}
          class="search-btn"
        >
          {searching ? "Searching..." : "Search"}
        </button>

        <button onclick={handleReset} disabled={searching} class="reset-btn">
          Reset
        </button>
      </div>
      <button
        onclick={() => {
          setHeatmapMode(!heatmapMode);
        }}
      >
        Turn Heatmap {heatmapMode ? "Off" : "On"}
      </button>
    </div>

    <div class="container">
      <div class="map">
        <Map height="650px" {renderData} showHeatmap={heatmapMode} />
      </div>
      <div class="chart">
        <Barchart
          labels={chartLabels}
          dataset={chartValue}
          labelName="Kepemilikan Gedung"
        />
      </div> 
      <div class="chart">
      <LineChart 
          labels={chartLabels}
          dataset={chartValue}
          labelName="Kepemilikan Gedung"
        />
      </div>
    </div>
  {/if}
</main>

<style>
  .filter-container {
    padding: 1.5em;
    display: flex;
    gap: 1em;
    align-items: flex-end;
    flex-wrap: wrap;
    background-color: #f5f5f5;
    border-radius: 8px;
    margin: 1em;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    color: #333;
  }

  .dropdown-group {
    display: flex;
    flex-direction: column;
    gap: 0.5em;
    min-width: 200px;
  }

  .dropdown-group label {
    font-weight: 600;
    font-size: 0.9em;
    color: #333;
  }

  .dropdown {
    padding: 0.75em;
    border: 1px solid #ccc;
    border-radius: 4px;
    font-size: 1em;
    background-color: white;
  }

  .dropdown:disabled {
    background-color: #f0f0f0;
    cursor: not-allowed;
  }

  .button-group {
    display: flex;
    gap: 0.5em;
    align-items: center;
  }

  .search-btn,
  .reset-btn {
    padding: 0.75em 1.5em;
    border: none;
    border-radius: 4px;
    font-size: 1em;
    cursor: pointer;
    transition: background-color 0.2s;
  }

  .search-btn {
    background-color: #007bff;
    color: white;
  }

  .search-btn:hover:not(:disabled) {
    background-color: #0056b3;
  }

  .search-btn:disabled {
    background-color: #ccc;
    cursor: not-allowed;
  }

  .reset-btn {
    background-color: #6c757d;
    color: white;
  }

  .reset-btn:hover:not(:disabled) {
    background-color: #5a6268;
  }

  .reset-btn:disabled {
    background-color: #ccc;
    cursor: not-allowed;
  }

  .map {
    height: 90em;
    width: 80em;
    padding: 1.5em;
    flex: 4;
  }

  select.dropdown {
    color: black;
  }

  /* Ensure the selected option also stays black */
  :global(select.dropdown option:checked) {
    color: black;
  }

  /* Optional: unselected items gray */
  :global(select.dropdown option) {
    color: #555;
  }

  .container {
    display: flex;
    gap: 1rem; /* spacing between map and chart */
  }

  .chart {
    flex: 1; /* both take equal width */
  }
</style>
