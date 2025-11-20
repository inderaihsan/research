<script lang="ts">
  import { onMount, onDestroy } from "svelte";
  import maplibregl from "maplibre-gl";
  import "maplibre-gl/dist/maplibre-gl.css";

  let {
    center = [106.79850764080264, -6.597378435400288] as [number, number], // Note: MapLibre uses [lng, lat]
    zoom = 7,
    height = "400px",
    onmapclick = () => {},
    renderData = null,
    showHeatmap = false, // Toggle between heatmap and points
  } = $props();

  let map;
  let container;
  const sourceId = "geojson-data";

  function handleClick(e) {
    const { lng, lat } = e.lngLat;
    onmapclick({ lng, lat });
  }

  function updateGeoJsonLayer() {
    if (!map) return;

    console.log("Updating GeoJSON layer with renderData:", renderData);

    // Check if source exists
    const source = map.getSource(sourceId);

    if (renderData && renderData.features && renderData.features.length > 0) {
      if (source) {
        // Update existing source
        console.log("Updating existing GeoJSON source");
        source.setData(renderData);
      } else {
        // Add new source and layers
        console.log("Adding new GeoJSON source and layers");
        map.addSource(sourceId, {
          type: "geojson",
          data: renderData,
        });

        // Add heatmap layer
        map.addLayer({
          id: "geojson-heatmap",
          type: "heatmap",
          source: sourceId,
          layout: {
            visibility: showHeatmap ? "visible" : "none",
          },
          paint: {
            // Increase the heatmap weight based on frequency and property magnitude
            "heatmap-weight": 1000,
            // Increase the heatmap color weight by zoom level
            // heatmap-intensity is a multiplier on top of heatmap-weight
            "heatmap-intensity": [
              "interpolate",
              ["linear"],
              ["zoom"],
              0,
              1,
              12,
              3,
            ],
            // Color ramp for heatmap. Domain is 0 (low) to 1 (high).
            "heatmap-color": [
              "interpolate",
              ["linear"],
              ["heatmap-density"],
              0,
              "rgba(33,102,172,0)",
              0.2,
              "rgb(103,169,207)",
              0.4,
              "rgb(209,229,240)",
              0.6,
              "rgb(253,219,199)",
              0.8,
              "rgb(239,138,98)",
              1,
              "rgb(178,24,43)",
            ],
            // Adjust the heatmap radius by zoom level
            "heatmap-radius": [
              "interpolate",
              ["linear"],
              ["zoom"],
              0,
              2,
              12,
              30,
            ],
            // Transition from heatmap to more transparent at higher zoom
            "heatmap-opacity": [
              "interpolate",
              ["linear"],
              ["zoom"],
              7,
              1,
              14,
              0.5,
            ],
          },
          filter: ["==", "$type", "Point"],
        });

        // Add a circle layer for points
        map.addLayer({
          id: "geojson-points",
          type: "circle",
          source: sourceId,
          layout: {
            visibility: showHeatmap ? "none" : "visible",
          },
          paint: {
            "circle-radius": 8,
            "circle-color": "#3887be",
            "circle-stroke-width": 2,
            "circle-stroke-color": "#ffffff",
          },
          filter: ["==", "$type", "Point"],
        });

        // Add popup on click (only works in marker mode)
        map.on("click", "geojson-points", (e) => {
          if (e.features && e.features.length > 0) {
            const feature = e.features[0];
            const coordinates = feature.geometry.coordinates.slice();
            const { nama_penerima, alamat_ordered } = feature.properties;

            // Ensure popup appears over the correct location
            while (Math.abs(e.lngLat.lng - coordinates[0]) > 180) {
              coordinates[0] += e.lngLat.lng > coordinates[0] ? 360 : -360;
            }

            new maplibregl.Popup()
              .setLngLat(coordinates)
              .setHTML(
                `
  <div style="color: black;">
    <strong>${nama_penerima}</strong><br/>
    ${alamat_ordered || ""}
  </div>
`
              )
              .addTo(map);
          }
        });

        // Change cursor on hover (only in marker mode)
        map.on("mouseenter", "geojson-points", () => {
          map.getCanvas().style.cursor = "pointer";
        });

        map.on("mouseleave", "geojson-points", () => {
          map.getCanvas().style.cursor = "";
        });
      }

      // Fit bounds to show all features
      const bounds = new maplibregl.LngLatBounds();
      renderData.features.forEach((feature) => {
        if (feature.geometry.type === "Point") {
          bounds.extend(feature.geometry.coordinates);
        }
      });

      if (!bounds.isEmpty()) {
        map.fitBounds(bounds, { padding: 50 });
      }
    } else if (source) {
      // Clear the data if renderData is empty
      console.log("Clearing GeoJSON data");
      source.setData({ type: "FeatureCollection", features: [] });
    }
  }

  // React to renderData changes
  $effect(() => {
    console.log("$effect triggered, renderData changed:", renderData);
    if (map && renderData) {
      console.log("Updating GeoJSON layer with new renderData");
      updateGeoJsonLayer();
    }
  });

  // React to showHeatmap changes - toggle layer visibility
  $effect(() => {
    console.log("$effect triggered, showHeatmap changed:", showHeatmap);
    if (
      map &&
      map.getLayer("geojson-heatmap") &&
      map.getLayer("geojson-points")
    ) {
      console.log("Toggling heatmap visibility:", showHeatmap);
      map.setLayoutProperty(
        "geojson-heatmap",
        "visibility",
        showHeatmap ? "visible" : "none"
      );
      map.setLayoutProperty(
        "geojson-points",
        "visibility",
        showHeatmap ? "none" : "visible"
      );
    }
  });

  onMount(() => {
    // Initialize map
    map = new maplibregl.Map({
      container,
      style: {
        version: 8,
        sources: {
          osm: {
            type: "raster",
            tiles: ["https://tile.openstreetmap.org/{z}/{x}/{y}.png"],
            tileSize: 256,
            attribution: "© OpenStreetMap contributors",
            maxzoom: 19,
          },
          satellite: {
            type: "raster",
            tiles: ["https://mt1.google.com/vt/lyrs=y&x={x}&y={y}&z={z}"],
            tileSize: 256,
            attribution: "© Google Maps",
            maxzoom: 19,
          },
        },
        layers: [
          {
            id: "osm-layer",
            type: "raster",
            source: "osm",
            layout: {
              visibility: "none", // Start with satellite visible
            },
          },
          {
            id: "satellite-layer",
            type: "raster",
            source: "satellite",
          },
        ],
      },
      center,
      zoom,
    });

    // Add navigation controls
    map.addControl(new maplibregl.NavigationControl(), "top-right");

    // Wait for map to load before adding data
    map.on("load", () => {
      updateGeoJsonLayer();
    });

    // Add click handler for the map (not on markers)
    map.on("click", (e) => {
      // Only trigger if not clicking on a feature
      const features = map.queryRenderedFeatures(e.point, {
        layers: ["geojson-points"],
      });
      if (features.length === 0) {
        handleClick(e);
      }
    });
  });

  onDestroy(() => {
    if (map) {
      map.remove();
    }
  });
</script>

<div
  bind:this={container}
  style="width:100%; height:{height}; border-radius:6px; overflow:hidden;"
></div>

<style>
  :global(.maplibregl-ctrl-top-right) {
    margin-top: 0.5rem;
    margin-right: 0.5rem;
  }
</style>
