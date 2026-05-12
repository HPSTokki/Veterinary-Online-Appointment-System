<script lang="ts">
	import './layout.css';
	import NavBar from '$lib/components/NavBar.svelte';
	import Footer from '$lib/components/Footer.svelte';
	import BookButton from '$lib/components/BookButton.svelte';
	import { onMount } from 'svelte';

	let { children } = $props();

	let showModal = $state(false);
	let activeTab = $state<'terms' | 'privacy' | 'cookies'>('terms');

	onMount(() => {
		const accepted = localStorage.getItem('dr-rosario-policies-accepted');
		if (!accepted) {
			showModal = true;
		}
	});

	function accept() {
		localStorage.setItem('dr-rosario-policies-accepted', 'true');
		showModal = false;
	}
</script>

<!-- Policies Popup Modal -->
{#if showModal}
	<div
		class="fixed inset-0 z-[9999] flex items-center justify-center bg-black/60 backdrop-blur-sm p-4"
	>
		<div
			class="relative flex w-full max-w-lg flex-col rounded-2xl bg-white shadow-2xl max-h-[90vh] overflow-hidden"
		>
			<!-- Header -->
			<div class="flex items-center justify-between bg-main px-5 py-4 rounded-t-2xl">
				<div>
					<h2 class="text-lg font-bold text-text-main leading-tight">Dr. Rosario Veterinary Clinic</h2>
					<p class="text-xs text-text-main/75 mt-0.5">Please review our policies before continuing</p>
				</div>
				<span class="text-2xl">🐾</span>
			</div>

			<!-- Tabs -->
			<div class="flex border-b border-slate-200 bg-slate-50">
				{#each ([['terms', 'Terms of Use'], ['privacy', 'Privacy Policy'], ['cookies', 'Cookie Policy']] as const) as [tab, label]}
					<button
						class="flex-1 px-2 py-2.5 text-xs font-semibold transition-all duration-150
							{activeTab === tab
								? 'border-b-2 border-main text-main bg-white'
								: 'text-slate-500 hover:text-slate-700 hover:bg-slate-100'}"
						onclick={() => (activeTab = tab)}
					>
						{label}
					</button>
				{/each}
			</div>

			<!-- Content -->
			<div class="flex-1 overflow-y-auto px-5 py-4 text-slate-700 text-sm leading-relaxed">

				{#if activeTab === 'terms'}
					<p class="text-xs text-slate-400 mb-3">Last Updated: May 2026</p>
					<p class="mb-3">Welcome to the Dr. Rosario Veterinary Clinic website. By accessing or using our website and appointment scheduling system, you agree to the following Terms of Use.</p>

					<h3 class="font-semibold text-slate-800 mt-4 mb-1">1. Acceptance of Terms</h3>
					<p class="mb-2">By using this website, you agree to comply with these Terms of Use and all applicable laws and regulations.</p>

					<h3 class="font-semibold text-slate-800 mt-4 mb-1">2. Services Provided</h3>
					<p class="mb-1">Our website provides access to:</p>
					<ul class="list-disc list-inside mb-2 text-slate-600 space-y-0.5">
						<li>Medical & Surgical Care</li>
						<li>Pet Grooming & Aesthetic Services</li>
						<li>Boarding and Temporary Care</li>
						<li>Pet Supplies and Accessories</li>
					</ul>

					<h3 class="font-semibold text-slate-800 mt-4 mb-1">3. User Responsibilities</h3>
					<p class="mb-1">Users agree to:</p>
					<ul class="list-disc list-inside mb-2 text-slate-600 space-y-0.5">
						<li>Provide accurate and complete information</li>
						<li>Use the website only for lawful purposes</li>
						<li>Avoid submitting false or misleading information</li>
						<li>Keep login credentials confidential</li>
					</ul>

					<h3 class="font-semibold text-slate-800 mt-4 mb-1">4. Appointment Scheduling</h3>
					<p class="mb-2">Appointments are subject to clinic confirmation. Dr. Rosario Veterinary Clinic reserves the right to reschedule, cancel, or refuse service for misuse.</p>

					<h3 class="font-semibold text-slate-800 mt-4 mb-1">5. Privacy and Data Protection</h3>
					<p class="mb-2">By using this website, you consent to the collection and use of your information in accordance with our Privacy Policy.</p>

					<h3 class="font-semibold text-slate-800 mt-4 mb-1">6. Intellectual Property</h3>
					<p class="mb-2">All website content, including logos, text, graphics, and system design, are the property of Dr. Rosario Veterinary Clinic unless otherwise stated.</p>

					<h3 class="font-semibold text-slate-800 mt-4 mb-1">7. Limitation of Liability</h3>
					<p class="mb-1">The clinic shall not be liable for:</p>
					<ul class="list-disc list-inside mb-2 text-slate-600 space-y-0.5">
						<li>Temporary website unavailability</li>
						<li>Technical errors or interruptions</li>
						<li>Data loss beyond reasonable control</li>
					</ul>

					<h3 class="font-semibold text-slate-800 mt-4 mb-1">8. Modifications</h3>
					<p class="mb-2">We may update these Terms at any time. Continued use means you accept the updated terms.</p>

				{:else if activeTab === 'privacy'}
					<p class="text-xs text-slate-400 mb-3">Last Updated: May 2026</p>
					<p class="mb-3">Dr. Rosario Veterinary Clinic values your privacy and is committed to protecting your personal information.</p>

					<h3 class="font-semibold text-slate-800 mt-4 mb-1">1. Information We Collect</h3>
					<p class="mb-1">We may collect:</p>
					<ul class="list-disc list-inside mb-2 text-slate-600 space-y-0.5">
						<li>Owner name, contact number, and email</li>
						<li>Pet information and appointment details</li>
						<li>Requested veterinary or grooming services</li>
					</ul>

					<h3 class="font-semibold text-slate-800 mt-4 mb-1">2. How We Use Information</h3>
					<p class="mb-1">Your information is used to:</p>
					<ul class="list-disc list-inside mb-2 text-slate-600 space-y-0.5">
						<li>Schedule and manage appointments</li>
						<li>Contact clients regarding bookings</li>
						<li>Maintain pet medical records</li>
						<li>Improve clinic operations and service</li>
					</ul>

					<h3 class="font-semibold text-slate-800 mt-4 mb-1">3. Data Protection</h3>
					<p class="mb-2">We implement reasonable security measures including login authentication, secure data storage, and system backups.</p>

					<h3 class="font-semibold text-slate-800 mt-4 mb-1">4. Sharing of Information</h3>
					<p class="mb-2">We do not sell or rent your personal information. Data is only shared with authorized clinic staff or when required by law.</p>

					<h3 class="font-semibold text-slate-800 mt-4 mb-1">5. Data Retention</h3>
					<p class="mb-2">Appointment and pet records may be retained for operational, medical, and legal purposes.</p>

					<h3 class="font-semibold text-slate-800 mt-4 mb-1">6. User Rights</h3>
					<p class="mb-1">You may request to:</p>
					<ul class="list-disc list-inside mb-2 text-slate-600 space-y-0.5">
						<li>Access your personal information</li>
						<li>Correct inaccurate information</li>
						<li>Request deletion of records (subject to legal requirements)</li>
					</ul>

				{:else}
					<p class="text-xs text-slate-400 mb-3">Last Updated: May 2026</p>
					<p class="mb-3">This Cookie Policy explains how Dr. Rosario Veterinary Clinic uses cookies and similar technologies on our website.</p>

					<h3 class="font-semibold text-slate-800 mt-4 mb-1">1. What Are Cookies?</h3>
					<p class="mb-2">Cookies are small text files stored on your device when you visit a website. They help improve website functionality and user experience.</p>

					<h3 class="font-semibold text-slate-800 mt-4 mb-1">2. Types of Cookies We Use</h3>
					<p class="mb-1 font-medium text-slate-700">Essential Cookies</p>
					<p class="mb-2 text-slate-600">Necessary for website navigation, login sessions, and appointment scheduling functions.</p>
					<p class="mb-1 font-medium text-slate-700">Performance Cookies</p>
					<p class="mb-2 text-slate-600">Help us understand website traffic, user interactions, and system performance.</p>
					<p class="mb-1 font-medium text-slate-700">Functional Cookies</p>
					<p class="mb-2 text-slate-600">Remember user preferences, saved settings, and appointment-related information.</p>

					<h3 class="font-semibold text-slate-800 mt-4 mb-1">3. Managing Cookies</h3>
					<p class="mb-2">You may disable cookies through your browser settings, though some website features may not function properly if cookies are disabled.</p>

					<h3 class="font-semibold text-slate-800 mt-4 mb-1">4. Third-Party Cookies</h3>
					<p class="mb-2">Some cookies may come from trusted third-party services used for hosting, analytics, or system support.</p>
				{/if}

			</div>

			<!-- Footer -->
			<div class="border-t border-slate-200 bg-slate-50 px-5 py-4 rounded-b-2xl">
				<p class="text-xs text-slate-500 mb-3 text-center">
					By clicking <strong>I Agree & Continue</strong>, you acknowledge that you have read and agree to our Terms of Use, Privacy Policy, and Cookie Policy.
				</p>
				<button
					onclick={accept}
					class="btn w-full bg-main text-text-main border-transparent hover:bg-sub font-semibold"
				>
					I Agree & Continue 🐾
				</button>
			</div>
		</div>
	</div>
{/if}

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
	<BookButton />
</div>
