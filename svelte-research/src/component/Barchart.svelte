<script>
  import { onMount, onDestroy } from "svelte";
  import Chart from "chart.js/auto";

  export let labels = []; // props from parent
  export let dataset = []; // props from parent
  export let labelName = "Some label";

  let canvasEl;
  let chartInstance;

  const chartOptions = {
    responsive: false,
    maintainAspectRatio: false,
  };

  onMount(() => {
    const ctx = canvasEl.getContext("2d");
    chartInstance = new Chart(ctx, {
      type: "bar",
      data: {
        labels: labels,
        datasets: [
          {
            label: labelName,
            data: dataset,
            backgroundColor: [
              "rgb(255, 99, 132)",
              "rgb(54, 162, 235)",
              "rgb(255, 205, 86)",
            ],
            borderColor: "rgba(75, 192, 192, 1)",
            borderWidth: 1,
          },
        ],
      },
      options: chartOptions,
    });
  });

  // Reactive: update chart when labels or dataset change
  $: if (chartInstance) {
    // avoid mutating original arrays; assign copies
    chartInstance.data.labels = Array.isArray(labels) ? [...labels] : [];
    if (chartInstance.data.datasets && chartInstance.data.datasets.length > 0) {
      chartInstance.data.datasets[0].data = Array.isArray(dataset)
        ? [...dataset]
        : [];
    }
    chartInstance.update();
  }

  onDestroy(() => {
    if (chartInstance) {
      chartInstance.destroy();
      chartInstance = null;
    }
  });
</script>

<canvas bind:this={canvasEl} style="width:100%; height:300px;"></canvas>
