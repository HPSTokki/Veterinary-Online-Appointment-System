<script lang="ts">
	import './layout.css';
	import NavBar from '$lib/components/NavBar.svelte';
	import Footer from '$lib/components/Footer.svelte';
	let { children } = $props();
</script>

<div class="flex flex-col justify-between min-h-screen">
	<header>
		<NavBar/>
	</header>

	<main class="flex-1 bg-text-main text-slate-900 flex flex-col justify-between">
		{@render children()}
	</main>

	<footer>
		<Footer />
	</footer>
</div>
