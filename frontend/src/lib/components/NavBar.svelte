<script lang="ts">
	import { page } from '$app/state';
	import { goto } from '$app/navigation';
	import VetLogo from '$lib/assets/VetLogo.png';
</script>

<div class="drawer">
	<input id="my-drawer-2" type="checkbox" class="drawer-toggle" />
	<div class="drawer-content flex flex-col">
		<!-- Navbar -->
		<div class="navbar w-full bg-main">
			<div class="flex-none lg:hidden">
				<label for="my-drawer-2" aria-label="open sidebar" class="btn btn-square btn-ghost">
					<svg
						xmlns="http://www.w3.org/2000/svg"
						fill="none"
						viewBox="0 0 24 24"
						class="inline-block h-6 w-6 stroke-current"
					>
						<path
							stroke-linecap="round"
							stroke-linejoin="round"
							stroke-width="2"
							d="M4 6h16M4 12h16M4 18h16"
						></path>
					</svg>
				</label>
			</div>
			<div class="flex flex-1 items-center px-2">
				<div class="mx-2 h-19 w-19 shrink-0 overflow-hidden object-cover">
					<img src={VetLogo} alt="Company Logo" class="h-full w-full" />
				</div>
				<div>
					<p>
						Dr. Rosario Vet Clinic <br />
						<span class="hidden text-xs lg:block"
							>237-A Malhacan, Meycauayan, Bulacan, 3020, Philippines</span
						>
					</p>
				</div>
			</div>
			<div class="hidden flex-none lg:block">
				<ul class="menu menu-horizontal">
					<!-- Navbar menu content here -->
					{#if !page.data.user}
						<li><a href="/#home">Home</a></li>
						<li><a href="/#about">About Us</a></li>
						<li><a href="/#services">Our Services</a></li>
						<li><a href="/#contact">Contact Us</a></li>
					{:else}
						<li><a href="/#home">Home</a></li>
						<li><a href="/#about">About Us</a></li>
						<li><a href="/#services">Our Services</a></li>
						<li><a href="/#contact">Contact Us</a></li>
						<li><a href="/profile">Profile</a></li>
					{/if}
				</ul>
			</div>
		</div>
		<!-- Page content here -->
	</div>
	<div class="drawer-side">
		<label for="my-drawer-2" aria-label="close sidebar" class="drawer-overlay"></label>
		<ul class="menu min-h-full w-80 bg-sub p-4">
			{#if !page.data.user}
				<li><a href="/#home">Home</a></li>
				<li><a href="/#about">About Us</a></li>
				<li><a href="/#services">Our Services</a></li>
				<li><a href="/#contact">Contact Us</a></li>
			{:else}
				<li><a href="/#home">Home</a></li>
				<li><a href="/#about">About Us</a></li>
				<li><a href="/#services">Our Services</a></li>
				<li><a href="/#contact">Contact Us</a></li>
				<li><a href="/profile">Profile</a></li>
			{/if}
		</ul>
	</div>
</div>
