<script lang="ts">
	import './layout.css';
	import NavBar from '$lib/components/NavBar.svelte';
	let { children } = $props();
</script>

<header>
	<NavBar />
</header>

<main>
{@render children()}
</main>

<footer>

</footer>