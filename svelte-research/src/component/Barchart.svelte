<script>
  import { onMount } from "svelte";
  import {
    Chart,
    Title,
    Tooltip,
    Legend,
    BarElement,
    CategoryScale,
    LinearScale,
    BarController,
  } from "chart.js";

  // Register the necessary components
  Chart.register(
    Title,
    Tooltip,
    Legend,
    BarElement,
    CategoryScale,
    LinearScale,
    BarController
  );

  export let chartData; // Data for your chart
  export let chartOptions; // Options for your chart
  export let chartType; // Type of chart (e.g., 'bar', 'line')

  let chartCanvas; // Reference to the canvas element

  onMount(() => {
    const ctx = chartCanvas.getContext("2d");
    new Chart(ctx, {
      type: chartType,
      data: chartData,
      options: chartOptions,
    });
  });
</script>

<canvas bind:this={chartCanvas}></canvas>
