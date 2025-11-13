<script lang="ts">
  import { onMount, onDestroy } from "svelte";
  import L from "leaflet";
  import "leaflet/dist/leaflet.css";

  let {
    center = [-6.175, 106.827] as [number, number],
    zoom = 10,
    height = "400px",
    onmapclick = () => {},
  } = $props();

  let map;
  let container;

  function handleClick(e) {
    const lat = e.latlng.lat;
    const lng = e.latlng.lng;
    onmapclick({ lng, lat });
  }

  onMount(() => {
    map = L.map(container, {
      center,
      zoom,
    });

    L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
      attribution: "© OpenStreetMap contributors",
      maxZoom: 19,
    }).addTo(map);

    map.on("click", handleClick);

    // Force resize after a short delay to ensure container has dimensions
    setTimeout(() => {
      map.invalidateSize();
    }, 100);

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
