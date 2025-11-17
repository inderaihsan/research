<script lang="ts">
  import { onMount, onDestroy } from "svelte";
  import L from "leaflet";
  import "leaflet/dist/leaflet.css";

  let {
    center = [-6.597378435400288, 106.79850764080264] as [number, number],
    zoom = 7,
    height = "400px",
    onmapclick = () => {},
    renderData = null,
  } = $props();

  let map;
  let container;
  let geoJsonLayer; // Keep reference to the GeoJSON layer

  function handleClick(e) {
    const lat = e.latlng.lat;
    const lng = e.latlng.lng;
    onmapclick({ lng, lat });
  }

  function updateGeoJsonLayer() {
    // Remove existing GeoJSON layer if it exists
    if (geoJsonLayer && map) {
      console.log("Removing existing GeoJSON layer");
      map.removeLayer(geoJsonLayer);
      geoJsonLayer = null;
    }

    // Add new GeoJSON layer if data exists
    console.log("Adding new GeoJSON layer with renderData:", renderData);
    if (renderData && renderData.features && renderData.features.length > 0 && map) {
      geoJsonLayer = L.geoJSON(renderData, {
        onEachFeature: (feature, layer) => {
          if (feature.properties && feature.properties.nama_penerima) {
            layer.bindPopup(
              `<strong>${feature.properties.nama_penerima}</strong><br/>
              ${feature.properties.alamat_ordered || ""}`
            );
          }
        },
      }).addTo(map);

      // Fit map to show all markers
      if (geoJsonLayer.getBounds().isValid()) {
        map.fitBounds(geoJsonLayer.getBounds(), { padding: [50, 50] });
      }
    }
  }

$effect(() => {
  console.log("$effect triggered, renderData changed:", renderData);
  if (map && renderData) {
    console.log("Updating GeoJSON layer with new renderData");
    updateGeoJsonLayer();
  }
})

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

    L.tileLayer("https://mt1.google.com/vt/lyrs=y&x={x}&y={y}&z={z}", {
      attribution: "© GoogleMaps contributors",
      maxZoom: 19,
    }).addTo(map);

    // Add initial GeoJSON layer
    updateGeoJsonLayer();

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

  // Watch for changes in renderData and update the layer
  $effect(() => {
    if (map && renderData) {
      updateGeoJsonLayer();
    }
  });

  onDestroy(() => {
    if (map) {
      map.off("click", handleClick);
      if (geoJsonLayer) {
        map.removeLayer(geoJsonLayer);
      }
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