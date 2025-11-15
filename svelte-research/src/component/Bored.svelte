<script>
  let count = $state(0);
  let emoticon = [
    "👾",
    "🤖",
    "👻",
    "💀",
    "☠️",
    "🦾",
    "🧠",
    "🧬",
    "🦠",
    "💥",
    "🧨",
    "⚡",
    "🔥",
    "🌈",
    "🌀",
    "🫨",
    "🫡",
    "🫥",
    "🤡",
    "🥸",
  ];

  let index = $state(0);
  const apikey = import.meta.env.OPENAI_API_KEY;

  // Get props (including any callbacks passed from parent)
  let { onincrement } = $props();
  let jokeretrieved = $state(null);

  function getRandomInteger(min, max) {
    min = Math.ceil(min); // Ensures min is an integer
    max = Math.floor(emoticon.length - 1); // Ensures max is an integer
    return Math.floor(Math.random() * (max - min + 1)) + min;
  }

  async function tellAJoke() {
    const response = await fetch("https://api.openai.com/v1/chat/completions", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${apikey}`,
      },
      body: JSON.stringify({
        model: "gpt-4",
        messages: [
          {
            role: "system",
            content:
              "Give a random facts! scientific one about the universe, math, scientist well something nerd",
          },
          {
            role: "user",
            content: `tell me a random facts`,
          },
        ],
      }),
    });

    if (!response.ok) throw new Error("Failed...");
    return await response.json();
  }

  function handleClick() {
    // Call the callback if it exists asd
    if (onincrement) {
      onincrement?.({ count });
      onincrement?.({ index });
    }

    index = getRandomInteger(0, 2);
    jokeretrieved = tellAJoke();
  }
</script>

<button onclick={handleClick}
  >Bored? click this button to generate a random emoticon</button
>

<h1>
  {emoticon[index]}
  {emoticon[index + 3]}
  {emoticon[index + 1]}
</h1>

{#if jokeretrieved}
  {#await jokeretrieved}
    <p>Loading jokesss...</p>
  {:then joke}
    <h3>" {joke.choices[0].message.content} "</h3>
  {:catch error}
    <p>Error: {error.message}</p>
  {/await}
{/if}
