<script lang="ts">
	import { MapPin, Phone, Clock } from '@lucide/svelte';
	import VetLogo from '$lib/assets/VetLogo.png';
</script>

<footer class="bg-main text-text-main">
	<div class="footer p-8 sm:footer-horizontal sm:p-10">
		<!-- Brand -->
		<aside class="max-w-xs">
			<div class="mb-2 h-16 w-16 overflow-hidden rounded-full">
				<img src={VetLogo} alt="Dr. Rosario Vet Clinic Logo" class="h-full w-full object-cover" />
			</div>
			<p class="text-base font-bold">Dr. Rosario Veterinary Clinic</p>
			<p class="mt-1 text-xs opacity-70">Providing reliable veterinary care since 1998</p>
			<div class="mt-3 flex flex-col gap-1.5 text-xs opacity-80">
				<span class="flex items-center gap-1.5">
					<MapPin size={13} />
					237-A Malhacan, Meycauayan, Bulacan
				</span>
				<span class="flex items-center gap-1.5">
					<Clock size={13} />
					Mon–Sat, 10:00 AM – 6:00 PM
				</span>
			</div>
		</aside>

		<!-- Company links -->
		<nav>
			<h6 class="footer-title text-text-main/60">Company</h6>
			<a href="/#about" class="link text-sm link-hover">About Us</a>
			<a href="/#services" class="link text-sm link-hover">Our Services</a>
			<a href="/#contact" class="link text-sm link-hover">Contact</a>
			<a href="/book" class="link text-sm link-hover">Book Now</a>
		</nav>

		<!-- Legal -->
		<nav>
			<h6 class="footer-title text-text-main/60">Legal</h6>
			<a href="/terms-and-condition" class="link text-sm link-hover">Terms of Use</a>
			<a href="/privacy-and-policy" class="link text-sm link-hover">Privacy Policy</a>
			<a href="/cookies" class="link text-sm link-hover">Cookie Policy</a>
		</nav>
	</div>

	<div class="border-t border-white/10 px-8 py-3 text-center text-xs opacity-50">
		© {new Date().getFullYear()} Dr. Rosario Veterinary Clinic. All rights reserved.
	</div>
</footer>
>
