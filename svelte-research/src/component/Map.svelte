<!-- <script>
  import { onMount, onDestroy } from "svelte";
  import L from "leaflet";

  export let renderData;

  let map;
  let mapContainer;

  onMount(() => {
    // Initialize map
    map = L.map(mapContainer).setView([-6.5946, 106.8134], 11);

    // Add tile layer
    L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
      attribution: "© OpenStreetMap contributors",
    }).addTo(map);

    // Add GeoJSON if data exists
    if (renderData && renderData.features) {
      const geoJsonLayer = L.geoJSON(renderData, {
        onEachFeature: (feature, layer) => {
          if (feature.properties && feature.properties.nama_penerima) {
            layer.bindPopup(
              `<strong>${feature.properties.nama_penerima}</strong>`
            );
          }
        },
      }).addTo(map);

      // Zoom to fit all markers
      if (geoJsonLayer.getBounds().isValid()) {
        map.fitBounds(geoJsonLayer.getBounds());
      }
    }

    // Force map to render properly
    setTimeout(() => map.invalidateSize(), 100);
  });

  onDestroy(() => {
    if (map) map.remove();
  });
</script>

<div bind:this={mapContainer} class="map"></div>

<style>
  .map {
    width: 100%;
    height: 600px; /* ⬅ THIS IS CRITICAL! */
  }
</style> -->

<script lang="ts">
  import { onMount, onDestroy } from "svelte";
  import L from "leaflet";
  import "leaflet/dist/leaflet.css";

  let {
    center = [-6.175, 106.827] as [number, number],
    zoom = 10,
    height = "400px",
    onmapclick = () => {},
    renderData = null,
  } = $props();

  let map;
  let container;

  function handleClick(e) {
    const lat = e.latlng.lat;
    const lng = e.latlng.lng;
    onmapclick({ lng, lat });
  }

  onMount(() => {
    // Initialize map
    map = L.map(container, {
      center,
      zoom,
    });

    // Add tile layer FIRST (base layer should be added before data layers)
    L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
      attribution: "© OpenStreetMap contributors",
      maxZoom: 19,
    }).addTo(map);

    // Add GeoJSON layer if data exists
    if (renderData && renderData.features && renderData.features.length > 0) {
      const geoJsonLayer = L.geoJSON(renderData, {
        onEachFeature: (feature, layer) => {
          if (feature.properties && feature.properties.nama_penerima) {
            layer.bindPopup(
              `<strong>${feature.properties.nama_penerima}</strong>`
            );
          }
        },
      }).addTo(map);

      // Fit map to show all markers
      if (geoJsonLayer.getBounds().isValid()) {
        map.fitBounds(geoJsonLayer.getBounds(), { padding: [50, 50] });
      }
    }

    // Add click handler
    map.on("click", handleClick);

    // Force resize after a short delay to ensure container has dimensions
    setTimeout(() => {
      map.invalidateSize();
    }, 100);

    // Observe container resize
    const ro = new ResizeObserver(() => map.invalidateSize());
    ro.observe(container);
    map._resizeObserver = ro;
  });

  onDestroy(() => {
    if (map) {
      map.off("click", handleClick);
      if (map._resizeObserver) {
        map._resizeObserver.disconnect();
      }
      map.remove();
    }
  });
</script>

<div
  bind:this={container}
  style="width:100%; height:{height}; border-radius:6px; overflow:hidden;"
></div>

<style>
  :global(.leaflet-control-zoom) {
    margin-top: 0rem;
  }
</style>
