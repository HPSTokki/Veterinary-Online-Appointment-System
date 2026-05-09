<script lang="ts">
	import { goto } from '$app/navigation';
	import { fly, fade, scale, slide } from 'svelte/transition';
	import { cubicOut } from 'svelte/easing';
	import { Eye, EyeOff, X, ShieldCheck, ShieldAlert } from '@lucide/svelte';

	let { open = $bindable(false) } = $props();
	let mode = $state<'login' | 'register'>('login');

	let showPasswordLogin = $state(false);
	let showPasswordRegister = $state(false);
	let showConfirmPassword = $state(false);
	let loginError = $state<string | null>(null);
	let registerError = $state<string | null>(null);
	let loading = $state(false);

	// --- Email validation (register) ---
	let regEmail = $state('');
	let regEmailTouched = $state(false);
	let regEmailValid = $derived(!regEmailTouched || /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(regEmail));

	// --- Password strength (register) ---
	let regPassword = $state('');
	let confirmPassword = $state('');
	let confirmTouched = $state(false);

	type Check = { label: string; pass: boolean };
	let passwordChecks = $derived<Check[]>([
		{ label: 'At least 8 characters', pass: regPassword.length >= 8 },
		{ label: 'One uppercase letter', pass: /[A-Z]/.test(regPassword) },
		{ label: 'One number', pass: /[0-9]/.test(regPassword) },
		{ label: 'One special character', pass: /[^A-Za-z0-9]/.test(regPassword) }
	]);

	let strengthScore = $derived(passwordChecks.filter((c) => c.pass).length);
	let strengthLabel = $derived(
		strengthScore === 0
			? ''
			: strengthScore <= 1
				? 'Weak'
				: strengthScore === 2
					? 'Fair'
					: strengthScore === 3
						? 'Good'
						: 'Strong'
	);
	let strengthColor = $derived(
		strengthScore <= 1
			? 'bg-red-400'
			: strengthScore === 2
				? 'bg-orange-400'
				: strengthScore === 3
					? 'bg-yellow-400'
					: 'bg-main'
	);
	let strengthTextColor = $derived(
		strengthScore <= 1
			? 'text-red-500'
			: strengthScore === 2
				? 'text-orange-500'
				: strengthScore === 3
					? 'text-yellow-600'
					: 'text-main'
	);
	let passwordsMatch = $derived(!confirmTouched || confirmPassword === regPassword);
	let canRegister = $derived(
		strengthScore >= 4 &&
			regEmailValid &&
			regEmail.length > 0 &&
			passwordsMatch &&
			confirmPassword.length > 0
	);

	// Shared input class
	const inp =
		'input w-full border-transparent bg-slate-100 text-main placeholder:text-main/40 focus:border-main focus:outline-none transition-colors';

	function resetState() {
		loginError = null;
		registerError = null;
		loading = false;
		regEmail = '';
		regEmailTouched = false;
		regPassword = '';
		confirmPassword = '';
		confirmTouched = false;
		showPasswordLogin = false;
		showPasswordRegister = false;
		showConfirmPassword = false;
	}

	function parseActionResult(result: any) {
		if (result?.type === 'failure') return { ok: false, data: result.data };
		if (result?.type === 'success') return { ok: true, data: result.data };
		return { ok: true, data: result };
	}

	async function handleLogin(event: Event) {
		event.preventDefault();
		loginError = null;
		loading = true;
		const form = event.target as HTMLFormElement;
		const response = await fetch('/auth?/login', {
			method: 'POST',
			body: new FormData(form),
			headers: { Accept: 'application/json' }
		});
		const { ok, data } = parseActionResult(await response.json());
		loading = false;
		if (ok) {
			open = false;
			goto('/profile');
		} else loginError = data?.message || 'Login failed. Check your credentials.';
	}

	async function handleRegister(event: Event) {
		event.preventDefault();
		if (!canRegister) return;
		registerError = null;
		loading = true;
		const form = event.target as HTMLFormElement;
		const response = await fetch('/auth?/register', {
			method: 'POST',
			body: new FormData(form),
			headers: { Accept: 'application/json' }
		});
		const { ok, data } = parseActionResult(await response.json());
		loading = false;
		if (ok) {
			open = false;
			goto('/profile');
		} else registerError = data?.message || 'Registration failed. Email may already be in use.';
	}
</script>

{#if open}
	<!-- Backdrop -->
	<div
		class="fixed inset-0 z-50 flex items-center justify-center p-4"
		role="presentation"
		onclick={() => {
			open = false;
			resetState();
		}}
		transition:fade={{ duration: 200 }}
	>
		<!-- Dim layer -->
		<div class="absolute inset-0 bg-black/60"></div>

		<!-- Card -->
		<div
			class="relative w-full max-w-sm overflow-hidden rounded-2xl bg-white shadow-2xl sm:max-w-md"
			role="presentation"
			onclick={(e) => e.stopPropagation()}
			transition:fly={{ y: 24, duration: 300, easing: cubicOut }}
		>
			<!-- Header -->
			<div class="flex items-center justify-between bg-main px-5 py-4">
				<div>
					<h2 class="text-base leading-tight font-bold text-text-main sm:text-lg">
						{mode === 'login' ? 'Welcome Back' : 'Create Account'}
					</h2>
					<p class="mt-0.5 text-xs text-text-main/70">Dr. Rosario Veterinary Clinic</p>
				</div>
				<button
					type="button"
					onclick={() => {
						open = false;
						resetState();
					}}
					class="btn btn-circle text-text-main/80 btn-ghost btn-sm hover:text-text-main"
					aria-label="Close"
				>
					<X size={18} />
				</button>
			</div>

			<!-- Tabs -->
			<div class="flex border-b border-gray-200">
				{#each ['login', 'register'] as const as tab (tab)}
					<button
						class="flex-1 py-3 text-sm font-semibold transition-colors duration-200
							{mode === tab ? 'border-b-2 border-main text-main' : 'text-gray-400 hover:text-gray-600'}"
						onclick={() => {
							mode = tab;
							resetState();
						}}
					>
						{tab === 'login' ? 'Login' : 'Register'}
					</button>
				{/each}
			</div>

			<!-- Body -->
			<div class="flex flex-col gap-4 px-5 py-5 pb-8 sm:pb-5">
				<!-- ===== LOGIN ===== -->
				{#if mode === 'login'}
					<div transition:fly={{ x: -20, duration: 250, easing: cubicOut }}>
						<form onsubmit={handleLogin} class="flex flex-col gap-3">
							{#if loginError}
								<div class="alert py-2 text-sm alert-error" transition:slide={{ duration: 200 }}>
									{loginError}
								</div>
							{/if}

							<label class="form-control w-full">
								<div class="label pb-1">
									<span class="label-text font-medium text-slate-500">Email</span>
								</div>
								<input
									name="email"
									type="email"
									placeholder="you@example.com"
									required
									class={inp}
								/>
							</label>

							<label class="form-control w-full">
								<div class="label pb-1">
									<span class="label-text font-medium text-slate-500">Password</span>
								</div>
								<div class="relative">
									<input
										name="password"
										type={showPasswordLogin ? 'text' : 'password'}
										placeholder="••••••••"
										required
										class="{inp} pr-10"
									/>
									<button
										type="button"
										class="absolute top-1/2 right-3 -translate-y-1/2 text-main/40 transition-colors hover:text-main"
										onclick={() => (showPasswordLogin = !showPasswordLogin)}
										aria-label="Toggle password"
									>
										{#if showPasswordLogin}<EyeOff size={16} />{:else}<Eye size={16} />{/if}
									</button>
								</div>
							</label>

							<button
								type="submit"
								disabled={loading}
								class="btn mt-1 btn-block border-none bg-main text-text-main hover:bg-sub disabled:opacity-60"
							>
								{#if loading}
									<span class="loading loading-sm loading-spinner"></span> Logging in...
								{:else}
									Login
								{/if}
							</button>
						</form>

						<div class="mt-3 text-center">
							<a
								href="/forgot-password"
								onclick={() => {
									open = false;
								}}
								class="text-xs text-main hover:underline"
							>
								Forgot your password?
							</a>
						</div>
					</div>

					<!-- ===== REGISTER ===== -->
				{:else}
					<div transition:fly={{ x: 20, duration: 250, easing: cubicOut }}>
						<form onsubmit={handleRegister} class="flex flex-col gap-3">
							{#if registerError}
								<div class="alert py-2 text-sm alert-error" transition:slide={{ duration: 200 }}>
									{registerError}
								</div>
							{/if}

							<!-- Email -->
							<label class="form-control w-full">
								<div class="label pb-1">
									<span class="label-text font-medium text-slate-500">Email</span>
								</div>
								<div class="relative">
									<input
										name="email"
										type="email"
										bind:value={regEmail}
										placeholder="you@example.com"
										required
										onblur={() => (regEmailTouched = true)}
										class="{inp} pr-10
											{regEmailTouched && !regEmailValid ? 'border border-red-400 focus:border-red-400' : ''}"
									/>
									{#if regEmailTouched}
										<span
											class="absolute top-1/2 right-3 -translate-y-1/2"
											transition:scale={{ duration: 150, start: 0.5 }}
										>
											{#if regEmailValid}
												<ShieldCheck size={15} class="text-main" />
											{:else}
												<ShieldAlert size={15} class="text-red-400" />
											{/if}
										</span>
									{/if}
								</div>
								{#if regEmailTouched && !regEmailValid}
									<div class="label pt-1" transition:slide={{ duration: 150 }}>
										<span class="label-text-alt text-red-500"
											>Please enter a valid email address.</span
										>
									</div>
								{/if}
							</label>

							<!-- Password -->
							<label class="form-control w-full">
								<div class="label pb-1">
									<span class="label-text font-medium text-slate-500">Password</span>
								</div>
								<div class="relative">
									<input
										name="password"
										type={showPasswordRegister ? 'text' : 'password'}
										bind:value={regPassword}
										placeholder="••••••••"
										required
										class="{inp} pr-10"
									/>
									<button
										type="button"
										class="absolute top-1/2 right-3 -translate-y-1/2 text-main/40 transition-colors hover:text-main"
										onclick={() => (showPasswordRegister = !showPasswordRegister)}
										aria-label="Toggle password"
									>
										{#if showPasswordRegister}<EyeOff size={16} />{:else}<Eye size={16} />{/if}
									</button>
								</div>
							</label>

							<!-- Strength panel -->
							{#if regPassword.length > 0}
								<div
									class="flex flex-col gap-2 rounded-xl bg-slate-100 p-3"
									transition:slide={{ duration: 200 }}
								>
									<!-- Bar -->
									<div class="flex gap-1">
										{#each passwordChecks as _, i (i)}
											<div
												class="h-1.5 flex-1 rounded-full transition-all duration-300
												{i < strengthScore ? strengthColor : 'bg-gray-200'}"
											></div>
										{/each}
									</div>
									{#if strengthLabel}
										<p class="text-xs font-semibold {strengthTextColor}">{strengthLabel}</p>
									{/if}
									<ul class="flex flex-col gap-1">
										{#each passwordChecks as check (check.label)}
											<li
												class="flex items-center gap-1.5 text-xs transition-colors duration-200
												{check.pass ? 'text-main' : 'text-gray-400'}"
											>
												{#if check.pass}
													<ShieldCheck size={12} class="shrink-0" />
												{:else}
													<ShieldAlert size={12} class="shrink-0" />
												{/if}
												{check.label}
											</li>
										{/each}
									</ul>
								</div>
							{/if}

							<!-- Confirm Password -->
							<label class="form-control w-full">
								<div class="label pb-1">
									<span class="label-text font-medium text-slate-500">Confirm Password</span>
								</div>
								<div class="relative">
									<input
										name="confirm_password"
										type={showConfirmPassword ? 'text' : 'password'}
										bind:value={confirmPassword}
										placeholder="••••••••"
										required
										onblur={() => (confirmTouched = true)}
										class="{inp} pr-10
											{confirmTouched && !passwordsMatch ? 'border border-red-400 focus:border-red-400' : ''}
											{confirmTouched && passwordsMatch && confirmPassword.length > 0 ? 'border border-main' : ''}"
									/>
									<button
										type="button"
										class="absolute top-1/2 right-3 -translate-y-1/2 text-main/40 transition-colors hover:text-main"
										onclick={() => (showConfirmPassword = !showConfirmPassword)}
										aria-label="Toggle confirm password"
									>
										{#if showConfirmPassword}<EyeOff size={16} />{:else}<Eye size={16} />{/if}
									</button>
								</div>
								{#if confirmTouched && !passwordsMatch}
									<div class="label pt-1" transition:slide={{ duration: 150 }}>
										<span class="label-text-alt text-red-500">Passwords do not match.</span>
									</div>
								{:else if confirmTouched && passwordsMatch && confirmPassword.length > 0}
									<div class="label pt-1" transition:slide={{ duration: 150 }}>
										<span class="label-text-alt flex items-center gap-1 text-main">
											<ShieldCheck size={12} /> Passwords match!
										</span>
									</div>
								{/if}
							</label>

							<button
								type="submit"
								disabled={loading || !canRegister}
								class="btn mt-1 btn-block border-none bg-main text-text-main hover:bg-sub disabled:opacity-60"
							>
								{#if loading}
									<span class="loading loading-sm loading-spinner"></span> Creating account...
								{:else}
									Create Account
								{/if}
							</button>
						</form>
					</div>
				{/if}
			</div>
		</div>
	</div>
{/if}
