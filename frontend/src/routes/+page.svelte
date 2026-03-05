<script lang="ts">
	import HeroBG from '$lib/assets/HeroBG.png';
	import HeroBG2 from '$lib/assets/HeroBG2.png';
	import VetServ1 from '$lib/assets/VetServ1.png';
	import VetServ2 from '$lib/assets/VetServ2.png';
	import VetServ3 from '$lib/assets/VetServ3.png';
	import VetServ4 from '$lib/assets/VetServ4.png';

	let showModal = () => true;

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

	const members = [
		{
			name: 'Dr. Al Rosario',
			desc: 'Owner and Chief Veterinarian of Dr. Rosario Veterinary Clinic'
		},
		{
			name: 'Merla Tolentino',
			desc: 'Co-Owner and Wife of Dr. Al Rosario'
		},
		{
			name: 'Mrs. Lala Tolentino',
			desc: 'Clinic Manager'
		},
		{
			name: 'Clinical Team',
			desc: 'Veterinarian, Veterinary, Assistants, and Surgical Support'
		},
		{
			name: 'Grooming and Boarding',
			desc: 'Groomers, Kennel Attendants, Care Staff'
		},
		{
			name: 'Admin & Support',
			desc: 'Front Desk, Billing, Supply Coordination'
		}
	];
</script>

<!-- Hero Section -->
<section id="home" class="flex flex-col gap-4 p-4 sm:p-6 md:p-8">
	<!-- Main Hero Banner -->
	<div
		style="background-image: url({HeroBG});"
		class="hero min-h-56 overflow-hidden rounded-2xl bg-cover bg-center sm:min-h-72 md:h-72"
	>
		<div class="bg-opacity-40 hero-overlay rounded-2xl"></div>
		<div class="hero-content px-4 text-center">
			<div class="max-w-xs sm:max-w-sm md:max-w-md">
				<h1 class="m-2 text-2xl leading-tight font-bold text-text-main sm:text-3xl md:text-4xl">
					Dr. Rosario Veterinary Clinic
				</h1>
				<p class="m-2 text-sm font-semibold text-text-main sm:text-base">
					Healing Paws. Happy Hearts.
				</p>
				<a href="#contact" class="btn m-2 border-main bg-main btn-ghost btn-sm sm:btn-md">
					Contact Us
				</a>
			</div>
		</div>
	</div>

	<!-- Tagline Banner -->
	<div
		style="background-image: url({HeroBG2});"
		class="hero min-h-32 overflow-hidden rounded-2xl bg-cover bg-center sm:min-h-40"
	>
		<div class="bg-opacity-50 hero-overlay rounded-2xl"></div>
		<div class="hero-content px-4 py-6 text-center sm:px-8">
			<p class="max-w-prose text-xs leading-relaxed font-medium text-white sm:text-sm md:text-base">
				Dr. Rosario Veterinary Clinic provides expert animal healthcare and professional grooming in
				Malhacan. From whelping assistance and major surgeries to pet boarding and a fully stocked
				accessory shop, we ensure your furry family members receive the best care under one roof.
			</p>
		</div>
	</div>

	<!-- Vision & Mission -->
	<div
		class="flex w-full flex-col overflow-hidden rounded-2xl bg-slate-200 text-center text-main md:flex-row"
	>
		<div class="card grid flex-1 place-items-center rounded-box p-4 sm:p-6">
			<h3 class="mb-2 text-lg font-semibold sm:text-xl">Our Vision</h3>
			<p class="max-w-sm text-xs leading-relaxed sm:text-sm">
				To be the most trusted and premier veterinary care partner in Bulacan, fostering a community
				where every pet enjoys a life of health, happiness, and compassionate well-being.
			</p>
		</div>
		<div class="divider my-0 divider-primary md:my-4 md:divider-horizontal">AND</div>
		<div class="card grid flex-1 place-items-center rounded-box p-4 sm:p-6">
			<h3 class="mb-2 text-lg font-semibold sm:text-xl">Our Mission</h3>
			<p class="max-w-sm text-xs leading-relaxed sm:text-sm">
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
	<h2 class="mb-2 text-center text-2xl font-bold sm:text-3xl">Our Services</h2>

	<div class="grid grid-cols-1 gap-4 sm:grid-cols-2 sm:gap-6">
		{#each services as service}
			<div
				class="card overflow-hidden rounded-2xl bg-base-100 shadow-md transition-shadow duration-300 hover:shadow-xl"
			>
				<!-- Service Image -->
				<figure class="h-40 overflow-hidden sm:h-48 md:h-56">
					<img
						src={service.img}
						alt={service.title}
						class="h-full w-full object-cover transition-transform duration-500 hover:scale-105"
					/>
				</figure>
				<!-- Service Info -->
				<div class="card-body p-4 sm:p-5">
					<h4 class="card-title text-base sm:text-lg">
						<span class="mr-1">{service.icon}</span>
						{service.title}
					</h4>
					<p class="text-xs leading-relaxed text-base-content/80 sm:text-sm">
						{service.desc}
					</p>
				</div>
			</div>
		{/each}
	</div>
</section>

<!-- About Us Section -->
<section id="about" class="flex flex-col gap-4 p-4 sm:p-6 md:p-8">
	<h2 class="mb-2 text-center text-2xl font-bold sm:text-3xl">Our Team</h2>
	<div class="grid grid-cols-1 gap-4 sm:grid-cols-2 sm:gap-6">
		{#each members as member}
			<div class="card items-center bg-main p-2 text-white shadow-sm lg:card-side">
				<div class="avatar avatar-placeholder">
					<div class="w-24 rounded-full bg-neutral text-neutral-content">
						<span class="text-3xl">{member.name.substr(0, 1)}</span>
					</div>
				</div>
				<div class="card-body items-center text-center">
					<h2 class="card-title">{member.name}</h2>
					<p>{member.desc}</p>
				</div>
			</div>
		{/each}
	</div>
</section>

<!-- Contact Us Section -->
<section id="contact" class="flex flex-col gap-4 p-4 text-text-main sm:p-6 md:p-8">
	<h2 class="mb-2 text-center text-2xl font-bold text-main sm:text-3xl">Get In Touch</h2>

	<div class="grid grid-cols-1 gap-4 sm:gap-6 lg:grid-cols-2">
		<!-- Contact Form Card -->
		<div class="card bg-main shadow-sm">
			<div class="card-body gap-3">
				<h3 class="card-title text-lg sm:text-xl">Contact Us</h3>

				<label class="form-control w-full">
					<div class="label"><span class="label-text text-xs sm:text-sm">Name</span></div>
					<input
						type="text"
						placeholder="Your full name"
						class="input-bordered input input-sm w-full bg-text-main text-slate-800 sm:input-md"
					/>
				</label>

				<label class="form-control w-full">
					<div class="label"><span class="label-text text-xs sm:text-sm">Contact No.</span></div>
					<input
						type="tel"
						placeholder="e.g. 09XX XXX XXXX"
						class="input-bordered input input-sm w-full bg-text-main text-slate-800 sm:input-md"
					/>
				</label>

				<label class="form-control w-full">
					<div class="label"><span class="label-text text-xs sm:text-sm">Email</span></div>
					<input
						type="email"
						placeholder="you@example.com"
						class="input-bordered input input-sm w-full bg-text-main text-slate-800 sm:input-md"
					/>
				</label>

				<label class="form-control w-full">
					<div class="label">
						<span class="label-text text-xs sm:text-sm">Service Inquiry</span>
					</div>
					<select
						class="select-bordered select w-full bg-text-main select-sm text-slate-800 sm:select-md"
					>
						<option disabled selected>Select a service</option>
						<option>Medical & Surgical Care</option>
						<option>Pet Grooming & Aesthetic Services</option>
						<option>Boarding and Temporary Care</option>
						<option>Pet Supplies and Accessories</option>
					</select>
				</label>

				<label class="form-control w-full">
					<div class="label">
						<span class="label-text text-xs sm:text-sm">Comment / Message</span>
					</div>
					<textarea
						class="textarea-bordered textarea w-full bg-text-main textarea-sm text-slate-800 sm:textarea-md"
						placeholder="Write your message here..."
						rows="4"
					></textarea>
				</label>

				<div class="mt-1 card-actions justify-end">
					<button class="btn w-full btn-sm btn-primary sm:w-auto sm:btn-md">Submit</button>
				</div>
			</div>
		</div>

		<!-- Map Card -->
		<div class="card bg-main shadow-sm">
			<div class="card-body gap-3 p-4 sm:p-6">
				<h3 class="card-title text-lg sm:text-xl">Visit Us</h3>
				<div class="h-64 w-full overflow-hidden rounded-xl sm:h-80 lg:h-full lg:min-h-96">
					<iframe
						src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d1404.164947048118!2d120.96635328512845!3d14.739992649382035!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x3397b235aece72a5%3A0x5259c55f50091034!2sDr.%20Rosario%20Veterinary%20Clinic!5e0!3m2!1sen!2sph!4v1772695295096!5m2!1sen!2sph"
						width="100%"
						height="100%"
						style="border:0;"
						loading="lazy"
						referrerpolicy="no-referrer-when-downgrade"
						title="Dr. Rosario Veterinary Clinic Map"
					></iframe>
				</div>
			</div>
		</div>
	</div>
</section>
