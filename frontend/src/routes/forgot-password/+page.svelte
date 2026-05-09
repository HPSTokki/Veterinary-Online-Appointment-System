<script lang="ts">
	import { enhance } from '$app/forms';
	import {
		Mail,
		KeyRound,
		Eye,
		EyeOff,
		ArrowLeft,
		CheckCircle,
		ChevronRight,
		ShieldCheck,
		ShieldAlert
	} from '@lucide/svelte';

	let { form } = $props();
	let step = $state<'request' | 'reset'>('request');
	let email = $state('');
	let showNewPassword = $state(false);

	// --- Email validation ---
	let emailTouched = $state(false);
	let emailValid = $derived(!emailTouched || /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email));

	// --- Password strength ---
	let newPassword = $state('');

	type Check = { label: string; pass: boolean };
	let passwordChecks = $derived<Check[]>([
		{ label: 'At least 8 characters', pass: newPassword.length >= 8 },
		{ label: 'One uppercase letter', pass: /[A-Z]/.test(newPassword) },
		{ label: 'One number', pass: /[0-9]/.test(newPassword) },
		{ label: 'One special character', pass: /[^A-Za-z0-9]/.test(newPassword) }
	]);

	let strengthScore = $derived(passwordChecks.filter((c) => c.pass).length);
	let strengthLabel = $derived(
		strengthScore === 0
			? ''
			: strengthScore <= 1
				? 'Weak'
				: strengthScore <= 2
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

	$effect(() => {
		if (form?.pin_sent) step = 'reset';
	});
</script>

<div class="flex min-h-[80vh] items-center justify-center px-4 py-12">
	<div class="w-full max-w-sm">
		<div class="card overflow-hidden bg-white shadow-xl">
			<!-- Header -->
			<div class="bg-main px-6 py-5">
				<div class="flex items-center gap-3">
					{#if step === 'request'}
						<Mail class="shrink-0 text-text-main/80" size={22} />
					{:else}
						<KeyRound class="shrink-0 text-text-main/80" size={22} />
					{/if}
					<div>
						<h1 class="text-lg leading-tight font-bold text-text-main">
							{step === 'request' ? 'Forgot Password' : 'Reset Password'}
						</h1>
						<p class="text-xs text-text-main/60">Dr. Rosario Veterinary Clinic</p>
					</div>
				</div>
			</div>

			<!-- Step indicator -->
			<div class="flex items-center border-b border-gray-100">
				<div
					class="flex flex-1 items-center justify-center gap-2 py-3
					{step === 'request' ? 'border-b-2 border-main text-main' : 'text-gray-400'}"
				>
					<div
						class="flex h-5 w-5 items-center justify-center rounded-full text-xs font-bold
						{step === 'request' ? 'bg-main text-white' : 'bg-gray-200 text-gray-500'}"
					>
						1
					</div>
					<span class="text-xs font-medium">Send PIN</span>
				</div>
				<ChevronRight size={14} class="shrink-0 text-gray-300" />
				<div
					class="flex flex-1 items-center justify-center gap-2 py-3
					{step === 'reset' ? 'border-b-2 border-main text-main' : 'text-gray-400'}"
				>
					<div
						class="flex h-5 w-5 items-center justify-center rounded-full text-xs font-bold
						{step === 'reset' ? 'bg-main text-white' : 'bg-gray-200 text-gray-500'}"
					>
						2
					</div>
					<span class="text-xs font-medium">New Password</span>
				</div>
			</div>

			<!-- Body -->
			<div class="flex flex-col gap-4 p-6">
				{#if form?.message && !form?.pin_sent && !form?.reset_success}
					<div class="alert py-2 text-sm alert-error">{form.message}</div>
				{/if}

				<!-- Success -->
				{#if form?.reset_success}
					<div class="flex flex-col items-center gap-3 py-4 text-center">
						<CheckCircle size={48} class="text-main" />
						<div>
							<p class="font-semibold text-gray-800">Password Reset!</p>
							<p class="mt-1 text-sm text-gray-500">You can now log in with your new password.</p>
						</div>
						<a href="/" class="btn mt-2 btn-block border-none bg-main text-text-main hover:bg-sub">
							Back to Login
						</a>
					</div>

					<!-- Step 1: Request PIN -->
				{:else if step === 'request'}
					<p class="text-sm text-gray-500">
						Enter your account email and we'll send you a 6-digit PIN.
					</p>

					{#if form?.pin_sent}
						<div class="alert py-2 text-sm alert-success">
							✓ PIN sent! Check your email then continue.
						</div>
					{/if}

					<form
						method="POST"
						action="?/request_pin"
						use:enhance={() => {
							return async ({ result, update }) => {
								await update();
								if (result.type === 'success' && result.data?.pin_sent) step = 'reset';
							};
						}}
						class="flex flex-col gap-4"
					>
						<label class="form-control w-full">
							<div class="label pb-1"><span class="label-text font-medium">Email</span></div>
							<div class="relative">
								<input
									name="email"
									type="email"
									bind:value={email}
									placeholder="you@example.com"
									required
									onblur={() => (emailTouched = true)}
									class="input-bordered input w-full bg-slate-100 pr-10 text-main transition-colors focus:outline-none
										{emailTouched && !emailValid ? 'border-red-400 focus:border-red-400' : 'focus:border-main'}"
								/>
								{#if emailTouched}
									<span class="absolute top-1/2 right-3 -translate-y-1/2">
										{#if emailValid}
											<ShieldCheck size={16} class="text-main" />
										{:else}
											<ShieldAlert size={16} class="text-red-400" />
										{/if}
									</span>
								{/if}
							</div>
							{#if emailTouched && !emailValid}
								<div class="label pt-1">
									<span class="label-text-alt text-red-500"
										>Please enter a valid email address.</span
									>
								</div>
							{/if}
						</label>

						<button
							type="submit"
							disabled={emailTouched && !emailValid}
							class="btn btn-block border-none bg-main text-text-main hover:bg-sub disabled:opacity-50"
						>
							Send PIN
						</button>
					</form>

					<button
						class="text-center text-xs text-main hover:underline"
						onclick={() => (step = 'reset')}
					>
						Already have a PIN? Skip →
					</button>

					<!-- Step 2: Reset with PIN -->
				{:else}
					<p class="text-sm text-gray-500">
						Enter the PIN from your email and choose a new password.
					</p>

					<form method="POST" action="?/reset_password" use:enhance class="flex flex-col gap-4">
						<label class="form-control w-full">
							<div class="label pb-1"><span class="label-text font-medium">Email</span></div>
							<input
								name="email"
								type="email"
								value={email}
								placeholder="you@example.com"
								required
								class="input-bordered input w-full bg-slate-100 text-main focus:border-main focus:outline-none"
							/>
						</label>

						<label class="form-control w-full">
							<div class="label pb-1"><span class="label-text font-medium">6-Digit PIN</span></div>
							<input
								name="pin"
								type="text"
								placeholder="000000"
								maxlength="6"
								inputmode="numeric"
								pattern="[0-9]*"
								required
								class="input-bordered input w-full bg-slate-100 text-center font-mono text-2xl tracking-[0.5em] text-main focus:border-main focus:outline-none"
							/>
						</label>

						<!-- New password with live strength -->
						<label class="form-control w-full">
							<div class="label pb-1"><span class="label-text font-medium">New Password</span></div>
							<div class="relative">
								<input
									name="new_password"
									type={showNewPassword ? 'text' : 'password'}
									bind:value={newPassword}
									placeholder="••••••••"
									required
									class="input-bordered input w-full bg-slate-100 pr-10 text-main focus:border-main focus:outline-none"
								/>
								<button
									type="button"
									aria-label="Toggle password"
									class="absolute top-1/2 right-3 -translate-y-1/2 text-gray-400 hover:text-gray-600"
									onclick={() => (showNewPassword = !showNewPassword)}
								>
									{#if showNewPassword}<EyeOff size={16} />{:else}<Eye size={16} />{/if}
								</button>
							</div>
						</label>

						<!-- Strength bar + label -->
						{#if newPassword.length > 0}
							<div class="flex flex-col gap-2 rounded-xl bg-gray-50 p-3">
								<!-- Bar -->
								<div class="flex gap-1">
									{#each passwordChecks as _, i (i)}
										<div
											class="h-1.5 flex-1 rounded-full transition-all duration-300
											{i < strengthScore ? strengthColor : 'bg-gray-200'}"
										></div>
									{/each}
								</div>

								<!-- Label -->
								{#if strengthLabel}
									<p class="text-xs font-semibold {strengthTextColor}">{strengthLabel}</p>
								{/if}

								<!-- Checklist -->
								<ul class="flex flex-col gap-1">
									{#each passwordChecks as check (check.label)}
										<li
											class="flex items-center gap-1.5 text-xs
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

						<button
							type="submit"
							disabled={strengthScore < 4}
							class="btn btn-block border-none bg-main text-text-main hover:bg-sub disabled:opacity-50"
						>
							Reset Password
						</button>
					</form>

					<button
						class="text-center text-xs text-gray-400 hover:underline"
						onclick={() => (step = 'request')}
					>
						← Resend PIN
					</button>
				{/if}
			</div>
		</div>

		{#if !form?.reset_success}
			<div class="mt-4 text-center">
				<a href="/" class="inline-flex items-center gap-1 text-sm text-main hover:underline">
					<ArrowLeft size={14} /> Back to Login
				</a>
			</div>
		{/if}
	</div>
</div>
