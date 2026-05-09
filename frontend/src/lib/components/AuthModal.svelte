<script lang="ts">
	import { goto } from '$app/navigation';
	import { Eye, EyeOff, X } from '@lucide/svelte';

	let { open = $bindable(false) } = $props();
	let mode = $state<'login' | 'register'>('login');

	let showPasswordLogin = $state(false);
	let showPasswordRegister = $state(false);
	let loginError = $state<string | null>(null);
	let registerError = $state<string | null>(null);
	let loading = $state(false);

	function resetState() {
		loginError = null;
		registerError = null;
		loading = false;
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
		} else {
			loginError = data?.message || 'Login failed. Check your credentials.';
		}
	}

	async function handleRegister(event: Event) {
		event.preventDefault();
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
		} else {
			registerError = data?.message || 'Registration failed. Email may already be in use.';
		}
	}
</script>

{#if open}
	<!-- Backdrop -->
	<div
		class="fixed inset-0 z-50 flex items-center justify-center bg-black/60 p-4"
		role="presentation"
		onclick={() => {
			open = false;
			resetState();
		}}
	>
		<!-- Sheet: slides up on mobile, centered card on sm+ -->
		<div
			class="w-full max-w-sm overflow-hidden rounded-2xl bg-white shadow-2xl sm:max-w-md"
			role="presentation"
			onclick={(e) => e.stopPropagation()}
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
				<button
					class="flex-1 py-3 text-sm font-semibold transition-colors {mode === 'login'
						? 'border-b-2 border-main text-main'
						: 'text-gray-400 hover:text-gray-600'}"
					onclick={() => {
						mode = 'login';
						resetState();
					}}
				>
					Login
				</button>
				<button
					class="flex-1 py-3 text-sm font-semibold transition-colors {mode === 'register'
						? 'border-b-2 border-main text-main'
						: 'text-gray-400 hover:text-gray-600'}"
					onclick={() => {
						mode = 'register';
						resetState();
					}}
				>
					Register
				</button>
			</div>

			<!-- Body -->
			<div class="flex flex-col gap-4 px-5 py-5 pb-8 sm:pb-5">
				{#if mode === 'login'}
					<form onsubmit={handleLogin} class="flex flex-col gap-4">
						{#if loginError}
							<div class="alert py-2 text-sm alert-error">{loginError}</div>
						{/if}

						<label class="form-control w-full">
							<div class="label pb-1">
								<span class="label-text font-medium text-main">Email</span>
							</div>
							<input
								name="email"
								type="email"
								placeholder="you@example.com"
								required
								class="input-bordered input w-full border-main/30 bg-slate-100 text-main focus:border-main focus:outline-none"
							/>
						</label>

						<label class="form-control w-full">
							<div class="label pb-1">
								<span class="label-text font-medium text-main">Password</span>
							</div>
							<div class="relative">
								<input
									name="password"
									type={showPasswordLogin ? 'text' : 'password'}
									placeholder="••••••••"
									required
									class="input-bordered input w-full border-main/30 bg-slate-100 text-main focus:border-main focus:outline-none"
								/>
								<button
									type="button"
									class="absolute top-1/2 right-3 -translate-y-1/2 text-gray-400 hover:text-gray-600"
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
							class="btn btn-block border-none bg-main text-text-main hover:bg-sub disabled:opacity-60"
						>
							{loading ? 'Logging in...' : 'Login'}
						</button>
					</form>

					<div class="text-center">
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
				{:else}
					<form onsubmit={handleRegister} class="flex flex-col gap-4">
						{#if registerError}
							<div class="alert py-2 text-sm alert-error">{registerError}</div>
						{/if}

						<label class="form-control w-full">
							<div class="label pb-1">
								<span class="label-text font-medium text-main">Email</span>
							</div>
							<input
								name="email"
								type="email"
								placeholder="you@example.com"
								required
								class="input-bordered input w-full border-main/30 bg-slate-100 text-main focus:border-main focus:outline-none"
							/>
						</label>

						<label class="form-control w-full">
							<div class="label pb-1">
								<span class="label-text font-medium text-main">Password</span>
							</div>
							<div class="relative">
								<input
									name="password"
									type={showPasswordRegister ? 'text' : 'password'}
									placeholder="••••••••"
									required
									class="input-bordered input w-full border-main/30 bg-slate-100 text-main focus:border-main focus:outline-none"
								/>
								<button
									type="button"
									class="absolute top-1/2 right-3 -translate-y-1/2 text-gray-400 hover:text-gray-600"
									onclick={() => (showPasswordRegister = !showPasswordRegister)}
									aria-label="Toggle password"
								>
									{#if showPasswordRegister}<EyeOff size={16} />{:else}<Eye size={16} />{/if}
								</button>
							</div>
						</label>

						<button
							type="submit"
							disabled={loading}
							class="btn btn-block border-none bg-main text-text-main hover:bg-sub disabled:opacity-60"
						>
							{loading ? 'Creating account...' : 'Create Account'}
						</button>
					</form>
				{/if}
			</div>
		</div>
	</div>
{/if}
