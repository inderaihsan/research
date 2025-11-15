<script>
  // Props
  let {
    placeholder = "Search for a location...",
    onsearch = () => {},
    onclear = () => {},
  } = $props();

  let searchValue = $state("");
  let isFocused = $state(false);

  function handleSearch(e) {
    e.preventDefault();
    if (searchValue.trim()) {
      onsearch(searchValue.trim());
    }
  }

  function handleClear() {
    searchValue = "";
    onclear();
  }

  function handleKeydown(e) {
    if (e.key === "Escape") {
      handleClear();
    }
  }
</script>

<form onsubmit={handleSearch} class="search-container">
  <div class="search-wrapper" class:focused={isFocused}>
    <!-- Search Icon -->
    <svg
      class="icon search-icon"
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
    >
      <circle cx="11" cy="11" r="8"></circle>
      <path d="m21 21-4.35-4.35"></path>
    </svg>

    <!-- Input -->
    <input
      type="text"
      bind:value={searchValue}
      onfocus={() => (isFocused = true)}
      onblur={() => (isFocused = false)}
      onkeydown={handleKeydown}
      {placeholder}
      class="search-input"
    />

    <!-- Clear Button -->
    {#if searchValue}
      <button
        type="button"
        onclick={handleClear}
        class="clear-btn"
        aria-label="Clear search"
      >
        <svg class="icon" viewBox="0 0 24 24" fill="none" stroke="currentColor">
          <line x1="18" y1="6" x2="6" y2="18"></line>
          <line x1="6" y1="6" x2="18" y2="18"></line>
        </svg>
      </button>
    {/if}

    <!-- Search Button -->
    <button
      type="submit"
      class="search-btn"
      disabled={!searchValue.trim()}
      aria-label="Search"
    >
      <svg class="icon" viewBox="0 0 24 24" fill="none" stroke="currentColor">
        <line x1="5" y1="12" x2="19" y2="12"></line>
        <polyline points="12 5 19 12 12 19"></polyline>
      </svg>
    </button>
  </div>
</form>

<style>
  .search-container {
    width: 100%;
    max-width: 600px;
  }

  .search-wrapper {
    position: relative;
    display: flex;
    align-items: center;
    background: white;
    border: 2px solid #e5e7eb;
    border-radius: 12px;
    padding: 0.75rem 1rem;
    transition: all 0.2s ease;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  }

  .search-wrapper:hover {
    border-color: #d1d5db;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.07);
  }

  .search-wrapper.focused {
    border-color: #3b82f6;
    box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
  }

  .icon {
    width: 20px;
    height: 20px;
    stroke-width: 2;
    flex-shrink: 0;
  }

  .search-icon {
    color: #9ca3af;
    margin-right: 0.75rem;
  }

  .search-input {
    flex: 1;
    border: none;
    outline: none;
    font-size: 1rem;
    color: #1f2937;
    background: transparent;
    min-width: 0;
  }

  .search-input::placeholder {
    color: #9ca3af;
  }

  .clear-btn,
  .search-btn {
    display: flex;
    align-items: center;
    justify-content: center;
    border: none;
    background: transparent;
    cursor: pointer;
    padding: 0.5rem;
    border-radius: 8px;
    transition: all 0.2s ease;
    margin-left: 0.5rem;
  }

  .clear-btn {
    color: #6b7280;
  }

  .clear-btn:hover {
    background: #f3f4f6;
    color: #374151;
  }

  .search-btn {
    color: white;
    background: #3b82f6;
  }

  .search-btn:hover:not(:disabled) {
    background: #2563eb;
    transform: translateX(2px);
  }

  .search-btn:disabled {
    background: #e5e7eb;
    color: #9ca3af;
    cursor: not-allowed;
  }

  .search-btn:active:not(:disabled) {
    transform: translateX(0);
  }

  /* Responsive */
  @media (max-width: 640px) {
    .search-wrapper {
      padding: 0.625rem 0.875rem;
    }

    .search-input {
      font-size: 0.938rem;
    }

    .icon {
      width: 18px;
      height: 18px;
    }
  }
</style>
