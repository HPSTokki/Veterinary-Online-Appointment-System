<script lang="ts">
	import { page } from '$app/state';
	import { Menu, X, PawPrint } from '@lucide/svelte';
	import VetLogo from '$lib/assets/VetLogo.png';

	let drawerOpen = $state(false);
</script>

<!-- Mobile drawer backdrop -->
{#if drawerOpen}
	<div
		class="fixed inset-0 z-40 bg-black/40 lg:hidden"
		role="presentation"
		onclick={() => (drawerOpen = false)}
	></div>
{/if}

<!-- Mobile Drawer -->
<div
	class="fixed top-0 left-0 z-50 h-full w-72 transform bg-main shadow-2xl transition-transform duration-300 lg:hidden {drawerOpen
		? 'translate-x-0'
		: '-translate-x-full'}"
>
	<div class="flex items-center justify-between border-b border-white/20 px-4 py-4">
		<div class="flex items-center gap-2">
			<PawPrint class="text-text-main" size={20} />
			<span class="text-sm font-bold text-text-main">Dr. Rosario Vet</span>
		</div>
		<button
			onclick={() => (drawerOpen = false)}
			class="btn btn-circle text-text-main btn-ghost btn-sm"
		>
			<X size={20} />
		</button>
	</div>
	<ul class="menu gap-1 p-4 text-text-main">
		<li><a href="/#home" onclick={() => (drawerOpen = false)}>Home</a></li>
		<li><a href="/#about" onclick={() => (drawerOpen = false)}>About Us</a></li>
		<li><a href="/#services" onclick={() => (drawerOpen = false)}>Our Services</a></li>
		<li><a href="/#contact" onclick={() => (drawerOpen = false)}>Contact Us</a></li>
		{#if page.data.user}
			<li><a href="/profile" onclick={() => (drawerOpen = false)}>My Profile</a></li>
		{/if}
	</ul>
</div>

<!-- Top Navbar -->
<div class="navbar w-full bg-main shadow-sm">
	<!-- Mobile hamburger -->
	<div class="flex-none lg:hidden">
		<button
			class="btn btn-square text-text-main btn-ghost"
			onclick={() => (drawerOpen = true)}
			aria-label="Open menu"
		>
			<Menu size={24} />
		</button>
	</div>

	<!-- Logo + Name -->
	<div class="flex flex-1 items-center gap-2 px-2">
		<div class="h-12 w-12 shrink-0 overflow-hidden rounded-full">
			<img src={VetLogo} alt="Dr. Rosario Vet Clinic Logo" class="h-full w-full object-cover" />
		</div>
		<div class="leading-tight text-text-main">
			<p class="text-sm font-bold">Dr. Rosario Vet Clinic</p>
			<p class="hidden text-xs opacity-70 lg:block">237-A Malhacan, Meycauayan, Bulacan</p>
		</div>
	</div>

	<!-- Desktop nav -->
	<div class="hidden flex-none lg:block">
		<ul class="menu menu-horizontal gap-1 text-text-main">
			<li><a href="/#home" class="rounded-lg hover:bg-white/10">Home</a></li>
			<li><a href="/#about" class="rounded-lg hover:bg-white/10">About Us</a></li>
			<li><a href="/#services" class="rounded-lg hover:bg-white/10">Our Services</a></li>
			<li><a href="/#contact" class="rounded-lg hover:bg-white/10">Contact Us</a></li>
			{#if page.data.user}
				<li><a href="/profile" class="rounded-lg hover:bg-white/10">My Profile</a></li>
			{/if}
		</ul>
	</div>
</div>
