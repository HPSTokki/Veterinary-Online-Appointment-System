<script lang="ts">
	import { goto } from '$app/navigation';

	let { open = $bindable(false) } = $props();
	let mode = $state<'login' | 'register'>('login');

	let showPasswordLogin = $state(false);
	let showPasswordRegister = $state(false);
	let loginError = $state<string | null>(null);
	let registerError = $state<string | null>(null);

	function resetState() {
		loginError = null;
		registerError = null;
	}

	function handleFocus(event: FocusEvent) {
		const target = event.target as HTMLElement;
		target.classList.add('border-[#2F5D4E]');
		target.classList.remove('border-gray-300');
	}

	function handleBlur(event: FocusEvent) {
		const target = event.target as HTMLElement;
		target.classList.add('border-gray-300');
		target.classList.remove('border-[#2F5D4E]');
	}

	function parseActionResult(result: any) {
		if (result?.type === 'failure') return { ok: false, data: result.data };
		if (result?.type === 'success') return { ok: true, data: result.data };
		return { ok: true, data: result };
	}

	async function handleLogin(event: Event) {
		event.preventDefault();
		loginError = null;
		const form = event.target as HTMLFormElement;
		const response = await fetch('/auth?/login', {
			method: 'POST',
			body: new FormData(form),
			headers: { Accept: 'application/json' }
		});
		const { ok, data } = parseActionResult(await response.json());
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
		const form = event.target as HTMLFormElement;
		const response = await fetch('/auth?/register', {
			method: 'POST',
			body: new FormData(form),
			headers: { Accept: 'application/json' }
		});
		const { ok, data } = parseActionResult(await response.json());
		if (ok) {
			open = false;
			goto('/profile');
		} else {
			registerError = data?.message || 'Registration failed. Email may already be in use.';
		}
	}
</script>

{#if open}
	<dialog
		class="fixed inset-0 z-50 m-0 flex h-full w-full max-w-none items-center justify-center border-none bg-black/60 p-4"
		onclick={() => {
			open = false;
			resetState();
		}}
		aria-modal="true"
		open
	>
		<div
			class="w-full max-w-md overflow-hidden rounded-2xl bg-white shadow-2xl"
			role="presentation"
			onclick={(e) => e.stopPropagation()}
		>
			<!-- Header -->
			<div class="flex items-center justify-between bg-[#2F5D4E] px-6 py-4">
				<div>
					<h2 class="text-lg leading-tight font-bold text-[#F2F8F4]">
						{mode === 'login' ? 'Welcome Back' : 'Create Account'}
					</h2>
					<p class="mt-0.5 text-xs text-[#F2F8F4]/70">Dr. Rosario Veterinary Clinic</p>
				</div>
				<button
					type="button"
					onclick={() => {
						open = false;
						resetState();
					}}
					class="text-xl leading-none text-[#F2F8F4]/70 transition-opacity hover:opacity-100"
					>✕</button
				>
			</div>

			<!-- Body -->
			<div class="flex flex-col gap-4 bg-white px-6 py-6">
				<!-- LOGIN -->
				{#if mode === 'login'}
					<form onsubmit={handleLogin} class="flex flex-col gap-4">
						{#if loginError}
							<div class="rounded-lg bg-red-50 px-3 py-2.5 text-sm text-red-600">{loginError}</div>
						{/if}
						<div class="flex flex-col gap-1">
							<label class="text-sm font-medium text-gray-900">Email</label>
							<input
								name="email"
								type="email"
								placeholder="you@example.com"
								required
								class="w-full rounded-lg border border-gray-300 bg-gray-50 px-3 py-2.5 text-sm text-gray-900 transition-colors outline-none focus:border-[#2F5D4E]"
								onfocus={handleFocus}
								onblur={handleBlur}
							/>
						</div>
						<div class="flex flex-col gap-1">
							<label class="text-sm font-medium text-gray-900">Password</label>
							<div class="relative">
								<input
									name="password"
									type={showPasswordLogin ? 'text' : 'password'}
									placeholder="••••••••"
									required
									class="w-full rounded-lg border border-gray-300 bg-gray-50 px-3 py-2.5 pr-10 text-sm text-gray-900 transition-colors outline-none focus:border-[#2F5D4E]"
									onfocus={handleFocus}
									onblur={handleBlur}
								/>
								<button
									type="button"
									class="absolute top-1/2 right-3 -translate-y-1/2 text-gray-500 hover:text-gray-700"
									onclick={() => (showPasswordLogin = !showPasswordLogin)}
								>
									{#if showPasswordLogin}
										<svg
											xmlns="http://www.w3.org/2000/svg"
											class="h-4 w-4"
											fill="none"
											viewBox="0 0 24 24"
											stroke="currentColor"
											><path
												stroke-linecap="round"
												stroke-linejoin="round"
												stroke-width="2"
												d="M13.875 18.825A10.05 10.05 0 0112 19c-4.478 0-8.268-2.943-9.543-7a9.97 9.97 0 011.563-3.029m5.858.908a3 3 0 114.243 4.243M9.878 9.878l4.242 4.242M9.88 9.88l-3.29-3.29m7.532 7.532l3.29 3.29M3 3l3.59 3.59m0 0A9.953 9.953 0 0112 5c4.478 0 8.268 2.943 9.543 7a10.025 10.025 0 01-4.132 4.411m0 0L21 21"
											/></svg
										>
									{:else}
										<svg
											xmlns="http://www.w3.org/2000/svg"
											class="h-4 w-4"
											fill="none"
											viewBox="0 0 24 24"
											stroke="currentColor"
											><path
												stroke-linecap="round"
												stroke-linejoin="round"
												stroke-width="2"
												d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"
											/><path
												stroke-linecap="round"
												stroke-linejoin="round"
												stroke-width="2"
												d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"
											/></svg
										>
									{/if}
								</button>
							</div>
						</div>
						<button
							type="submit"
							class="w-full cursor-pointer rounded-lg border-none bg-[#2F5D4E] py-2.5 text-sm font-semibold text-[#F2F8F4] transition-colors hover:bg-[#2E6F40]"
						>
							Login
						</button>
					</form>
					<div class="flex items-center justify-between">
						<a
							href="/forgot-password"
							onclick={() => {
								open = false;
							}}
							class="text-xs text-[#2F5D4E] hover:underline"
						>
							Forgot Password?
						</a>
						<button
							class="text-xs text-[#2F5D4E] hover:underline"
							onclick={() => {
								mode = 'register';
								resetState();
							}}
						>
							No account? Register
						</button>
					</div>

					<!-- REGISTER -->
				{:else}
					<form onsubmit={handleRegister} class="flex flex-col gap-4">
						{#if registerError}
							<div class="rounded-lg bg-red-50 px-3 py-2.5 text-sm text-red-600">
								{registerError}
							</div>
						{/if}
						<div class="flex flex-col gap-1">
							<label class="text-sm font-medium text-gray-900">Email</label>
							<input
								name="email"
								type="email"
								placeholder="you@example.com"
								required
								class="w-full rounded-lg border border-gray-300 bg-gray-50 px-3 py-2.5 text-sm text-gray-900 transition-colors outline-none focus:border-[#2F5D4E]"
								onfocus={handleFocus}
								onblur={handleBlur}
							/>
						</div>
						<div class="flex flex-col gap-1">
							<label class="text-sm font-medium text-gray-900">Password</label>
							<div class="relative">
								<input
									name="password"
									type={showPasswordRegister ? 'text' : 'password'}
									placeholder="••••••••"
									required
									class="w-full rounded-lg border border-gray-300 bg-gray-50 px-3 py-2.5 pr-10 text-sm text-gray-900 transition-colors outline-none focus:border-[#2F5D4E]"
									onfocus={handleFocus}
									onblur={handleBlur}
								/>
								<button
									type="button"
									class="absolute top-1/2 right-3 -translate-y-1/2 text-gray-500 hover:text-gray-700"
									onclick={() => (showPasswordRegister = !showPasswordRegister)}
								>
									{#if showPasswordRegister}
										<svg
											xmlns="http://www.w3.org/2000/svg"
											class="h-4 w-4"
											fill="none"
											viewBox="0 0 24 24"
											stroke="currentColor"
											><path
												stroke-linecap="round"
												stroke-linejoin="round"
												stroke-width="2"
												d="M13.875 18.825A10.05 10.05 0 0112 19c-4.478 0-8.268-2.943-9.543-7a9.97 9.97 0 011.563-3.029m5.858.908a3 3 0 114.243 4.243M9.878 9.878l4.242 4.242M9.88 9.88l-3.29-3.29m7.532 7.532l3.29 3.29M3 3l3.59 3.59m0 0A9.953 9.953 0 0112 5c4.478 0 8.268 2.943 9.543 7a10.025 10.025 0 01-4.132 4.411m0 0L21 21"
											/></svg
										>
									{:else}
										<svg
											xmlns="http://www.w3.org/2000/svg"
											class="h-4 w-4"
											fill="none"
											viewBox="0 0 24 24"
											stroke="currentColor"
											><path
												stroke-linecap="round"
												stroke-linejoin="round"
												stroke-width="2"
												d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"
											/><path
												stroke-linecap="round"
												stroke-linejoin="round"
												stroke-width="2"
												d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"
											/></svg
										>
									{/if}
								</button>
							</div>
						</div>
						<button
							type="submit"
							class="w-full cursor-pointer rounded-lg border-none bg-[#2F5D4E] py-2.5 text-sm font-semibold text-[#F2F8F4] transition-colors hover:bg-[#2E6F40]"
						>
							Create Account
						</button>
					</form>
					<div class="text-center">
						<button
							class="text-xs text-[#2F5D4E] hover:underline"
							onclick={() => {
								mode = 'login';
								resetState();
							}}
						>
							Already have an account? Login
						</button>
					</div>
				{/if}
			</div>
		</div>
	</dialog>
{/if}
