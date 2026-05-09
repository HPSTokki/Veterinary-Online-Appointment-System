<script lang="ts">
	import { enhance } from '$app/forms';

	let { form } = $props();
	let step = $state<'request' | 'reset'>('request');
	let email = $state('');
	let showNewPassword = $state(false);

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
</script>

<div class="flex min-h-[70vh] items-center justify-center px-4 py-12">
	<div class="w-full max-w-md">
		<!-- Card -->
		<div class="overflow-hidden rounded-2xl bg-white shadow-xl">
			<!-- Header -->
			<div class="bg-[#2F5D4E] px-6 py-5">
				<h1 class="text-xl leading-tight font-bold text-[#F2F8F4]">
					{step === 'request' ? 'Forgot Password' : 'Reset Password'}
				</h1>
				<p class="mt-1 text-xs text-[#F2F8F4]/70">Dr. Rosario Veterinary Clinic</p>
			</div>

			<div class="flex flex-col gap-4 px-6 py-6">
				<!-- Step indicator -->
				<div class="mb-1 flex items-center gap-2">
					<div class="flex items-center gap-1.5">
						<div
							class="flex h-6 w-6 items-center justify-center rounded-full text-xs font-bold
                            {step === 'request'
								? 'bg-[#2F5D4E] text-white'
								: 'bg-[#2F5D4E]/20 text-[#2F5D4E]'}"
						>
							1
						</div>
						<span class="text-xs text-gray-500">Send PIN</span>
					</div>
					<div class="h-px flex-1 bg-gray-200"></div>
					<div class="flex items-center gap-1.5">
						<div
							class="flex h-6 w-6 items-center justify-center rounded-full text-xs font-bold
                            {step === 'reset'
								? 'bg-[#2F5D4E] text-white'
								: 'bg-gray-100 text-gray-400'}"
						>
							2
						</div>
						<span class="text-xs text-gray-500">New Password</span>
					</div>
				</div>

				<!-- Error / success banners -->
				{#if form?.message && !form?.reset_success && !form?.pin_sent}
					<div class="rounded-lg bg-red-50 px-3 py-2.5 text-sm text-red-600">{form.message}</div>
				{/if}
				{#if form?.pin_sent}
					<div class="rounded-lg bg-green-50 px-3 py-2.5 text-sm text-green-700">
						✓ PIN sent! Check your email then enter it below.
					</div>
				{/if}
				{#if form?.reset_success}
					<div class="rounded-lg bg-green-50 px-3 py-2.5 text-sm text-green-700">
						✓ Password reset successfully!
					</div>
					<a
						href="/"
						class="block w-full rounded-lg bg-[#2F5D4E] py-2.5 text-center text-sm font-semibold text-[#F2F8F4] transition-colors hover:bg-[#2E6F40]"
					>
						Back to Login
					</a>
				{:else}
					<!-- STEP 1: Request PIN -->
					{#if step === 'request'}
						<p class="text-sm text-gray-500">
							Enter your account email and we'll send you a 6-digit PIN.
						</p>
						<form
							method="POST"
							action="?/request_pin"
							use:enhance={() => {
								return async ({ result, update }) => {
									await update();
									if (result.type === 'success' && result.data?.pin_sent) {
										step = 'reset';
									}
								};
							}}
							class="flex flex-col gap-4"
						>
							<div class="flex flex-col gap-1">
								<label class="text-sm font-medium text-gray-900">Email</label>
								<input
									name="email"
									type="email"
									bind:value={email}
									placeholder="you@example.com"
									required
									class="w-full rounded-lg border border-gray-300 bg-gray-50 px-3 py-2.5 text-sm text-gray-900 transition-colors outline-none focus:border-[#2F5D4E]"
									onfocus={handleFocus}
									onblur={handleBlur}
								/>
							</div>
							<button
								type="submit"
								class="w-full cursor-pointer rounded-lg border-none bg-[#2F5D4E] py-2.5 text-sm font-semibold text-[#F2F8F4] transition-colors hover:bg-[#2E6F40]"
							>
								Send PIN
							</button>
						</form>
						<button
							class="text-center text-xs text-gray-400 hover:underline"
							onclick={() => (step = 'reset')}
						>
							Already have a PIN? Skip →
						</button>

						<!-- STEP 2: Reset with PIN -->
					{:else}
						<p class="text-sm text-gray-500">
							Enter the 6-digit PIN from your email along with your new password.
						</p>
						<form method="POST" action="?/reset_password" use:enhance class="flex flex-col gap-4">
							<div class="flex flex-col gap-1">
								<label class="text-sm font-medium text-gray-900">Email</label>
								<input
									name="email"
									type="email"
									value={email}
									placeholder="you@example.com"
									required
									class="w-full rounded-lg border border-gray-300 bg-gray-50 px-3 py-2.5 text-sm text-gray-900 transition-colors outline-none focus:border-[#2F5D4E]"
									onfocus={handleFocus}
									onblur={handleBlur}
								/>
							</div>

							<div class="flex flex-col gap-1">
								<label class="text-sm font-medium text-gray-900">6-Digit PIN</label>
								<input
									name="pin"
									type="text"
									placeholder="000000"
									maxlength="6"
									required
									class="w-full rounded-lg border border-gray-300 bg-gray-50 px-3 py-2.5 text-center font-mono text-2xl tracking-[0.5em] text-gray-900 transition-colors outline-none focus:border-[#2F5D4E]"
									onfocus={handleFocus}
									onblur={handleBlur}
								/>
							</div>

							<div class="flex flex-col gap-1">
								<label class="text-sm font-medium text-gray-900">New Password</label>
								<div class="relative">
									<input
										name="new_password"
										type={showNewPassword ? 'text' : 'password'}
										placeholder="••••••••"
										required
										class="w-full rounded-lg border border-gray-300 bg-gray-50 px-3 py-2.5 pr-10 text-sm text-gray-900 transition-colors outline-none focus:border-[#2F5D4E]"
										onfocus={handleFocus}
										onblur={handleBlur}
									/>
									<button
										type="button"
										class="absolute top-1/2 right-3 -translate-y-1/2 text-gray-500 hover:text-gray-700"
										onclick={() => (showNewPassword = !showNewPassword)}
									>
										{showNewPassword ? '🙈' : '👁️'}
									</button>
								</div>
							</div>

							<button
								type="submit"
								class="w-full cursor-pointer rounded-lg border-none bg-[#2F5D4E] py-2.5 text-sm font-semibold text-[#F2F8F4] transition-colors hover:bg-[#2E6F40]"
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
				{/if}
			</div>
		</div>

		<p class="mt-4 text-center text-sm text-gray-500">
			Remembered it?
			<a href="/" class="font-medium text-[#2F5D4E] hover:underline">Back to Login</a>
		</p>
	</div>
</div>
