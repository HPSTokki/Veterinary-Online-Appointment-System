<script lang="ts">
	import HeroBG from '$lib/assets/HeroBG.png';
	import HeroBG2 from '$lib/assets/HeroBG2.png';
	import VetServ1 from '$lib/assets/VetServ1.png';
	import VetServ2 from '$lib/assets/VetServ2.png';
	import VetServ3 from '$lib/assets/VetServ3.png';
	import VetServ4 from '$lib/assets/VetServ4.png';

	const services = [
		{
			img: VetServ1,
			icon: '🩺',
			title: 'Medical & Surgical Care',
			desc: 'Comprehensive veterinary treatment for dogs and cats, including consultations, diagnostics, surgical procedures, whelping assistance, confinement care, and preventive services like deworming and vaccinations.'
		},
		{
			img: VetServ2,
			icon: '✂️',
			title: 'Pet Grooming & Aesthetic Services',
			desc: 'Professional grooming, ear cropping, tail docking, and hygiene maintenance to keep pets clean, healthy, and well-presented.'
		},
		{
			img: VetServ3,
			icon: '🏠',
			title: 'Boarding and Temporary Care',
			desc: 'Safe and supervised boarding/confinement services for pets whose owners are traveling or need short-term care assistance.'
		},
		{
			img: VetServ4,
			icon: '🛍️',
			title: 'Pet Supplies and Accessories',
			desc: 'Retail of essential pet products and accessories, providing a convenient one-stop solution for pet owners alongside clinical services.'
		}
	];
</script>

<!-- Hero Section -->
<section id="home" class="flex flex-col gap-4 p-4 sm:p-6 md:p-8">
	<!-- Main Hero Banner -->
	<div
		style="background-image: url({HeroBG});"
		class="hero min-h-56 sm:min-h-72 md:h-72 overflow-hidden rounded-2xl bg-cover bg-center"
	>
		<div class="hero-overlay bg-opacity-40 rounded-2xl"></div>
		<div class="hero-content text-center px-4">
			<div class="max-w-xs sm:max-w-sm md:max-w-md">
				<h1 class="m-2 text-2xl sm:text-3xl md:text-4xl font-bold text-text-main leading-tight">
					Dr. Rosario Veterinary Clinic
				</h1>
				<p class="m-2 text-sm sm:text-base font-semibold text-text-main">
					Healing Paws. Happy Hearts.
				</p>
				<a
					href="#contact"
					class="btn m-2 border-main bg-main btn-ghost btn-sm sm:btn-md"
				>
					Contact Us
				</a>
			</div>
		</div>
	</div>

	<!-- Tagline Banner -->
	<div
		style="background-image: url({HeroBG2});"
		class="hero min-h-32 sm:min-h-40 overflow-hidden rounded-2xl bg-cover bg-center"
	>
		<div class="hero-overlay bg-opacity-50 rounded-2xl"></div>
		<div class="hero-content text-center px-4 sm:px-8 py-6">
			<p class="text-xs sm:text-sm md:text-base max-w-prose text-white font-medium leading-relaxed">
				Dr. Rosario Veterinary Clinic provides expert animal healthcare and professional grooming in
				Malhacan. From whelping assistance and major surgeries to pet boarding and a fully stocked
				accessory shop, we ensure your furry family members receive the best care under one roof.
			</p>
		</div>
	</div>

	<!-- Vision & Mission -->
	<div class="flex w-full flex-col md:flex-row overflow-hidden rounded-2xl bg-slate-200 text-center text-main">
		<div class="card flex-1 grid place-items-center rounded-box p-4 sm:p-6">
			<h3 class="text-lg sm:text-xl font-semibold mb-2">Our Vision</h3>
			<p class="text-xs sm:text-sm leading-relaxed max-w-sm">
				To be the most trusted and premier veterinary care partner in Bulacan, fostering a community
				where every pet enjoys a life of health, happiness, and compassionate well-being.
			</p>
		</div>
		<div class="divider divider-primary my-0 md:divider-horizontal md:my-4">AND</div>
		<div class="card flex-1 grid place-items-center rounded-box p-4 sm:p-6">
			<h3 class="text-lg sm:text-xl font-semibold mb-2">Our Mission</h3>
			<p class="text-xs sm:text-sm leading-relaxed max-w-sm">
				To provide comprehensive, accessible, and high-quality veterinary medical and grooming
				services through a family-oriented approach. We are dedicated to treating every animal with
				kindness, educating pet owners on responsible care, and ensuring peace of mind for families
				who entrust their beloved companions to us.
			</p>
		</div>
	</div>
</section>

<!-- Services Section -->
<section id="services" class="flex flex-col gap-4 p-4 sm:p-6 md:p-8">
	<h2 class="text-2xl sm:text-3xl font-bold text-center mb-2">Our Services</h2>

	<div class="grid grid-cols-1 sm:grid-cols-2 gap-4 sm:gap-6">
		{#each services as service}
			<div class="card rounded-2xl overflow-hidden shadow-md bg-base-100 hover:shadow-xl transition-shadow duration-300">
				<!-- Service Image -->
				<figure class="h-40 sm:h-48 md:h-56 overflow-hidden">
					<img
						src={service.img}
						alt={service.title}
						class="w-full h-full object-cover hover:scale-105 transition-transform duration-500"
					/>
				</figure>
				<!-- Service Info -->
				<div class="card-body p-4 sm:p-5">
					<h4 class="card-title text-base sm:text-lg">
						<span class="mr-1">{service.icon}</span>
						{service.title}
					</h4>
					<p class="text-xs sm:text-sm text-base-content/80 leading-relaxed">
						{service.desc}
					</p>
				</div>
			</div>
		{/each}
	</div>
</section>

<!-- About Us Section -->
<section id="about"></section>

<!-- Contact Us Section -->
<section id="contact"></section>