<!-- appointment/+page.svelte -->
<script lang="ts">
	import { enhance } from '$app/forms';
	import { getAvailableSlots } from '$lib/api/appointment';
    import { goto, invalidateAll } from '$app/navigation';

	interface AppointmentData {
		success?: boolean;
		message?: string;
		appointment?: {
			service_name: string;
			appointment_date: string;
			start_time: string;
			end_time: string;
		};
	}
	let { data, form }: { data: any; form: AppointmentData | null } = $props();

	let selectedPet = $state<number | null>(null);
	let selectedService = $state<number | null>(null);
	let selectedDate = $state<string | null>(null);
	let selectedSlot = $state<{ start_time: string; end_time: string } | null>(null);

	let slots = $state<{ start_time: string; end_time: string }[]>([]);
	let loadingSlots = $state(false);
	let confirmed = $derived(false);

	$effect(() => {
		if (form?.success) confirmed = true;
	});

	async function fetchSlots() {
		if (!selectedService || !selectedDate) return;
		loadingSlots = true;
		slots = await getAvailableSlots(data.token, selectedService, selectedDate);
		selectedSlot = null;
		loadingSlots = false;
	}

	function formatTime(dt: string) {
		return new Date(dt).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
	}

	function formatDate(dt: string) {
		return new Date(dt).toLocaleDateString([], {
			weekday: 'long',
			year: 'numeric',
			month: 'long',
			day: 'numeric'
		});
	}

    async function resetBooking() {
        confirmed = false
        selectedPet = null
        selectedService = null
        selectedDate = null
        selectedSlot = null
        slots = []
        await invalidateAll()
    }

	const tomorrow = new Date();
	tomorrow.setDate(tomorrow.getDate() + 1);
	const minDate = tomorrow.toISOString().split('T')[0];
</script>

{#if confirmed || form?.success}
	<div class="mx-auto mt-12 flex max-w-lg flex-col items-center gap-4 p-6 text-center">
		<div class="text-6xl">🐾</div>
		<h2 class="text-2xl font-bold text-main!">Appointment Booked!</h2>
		<p class="text-sm text-main/60!">We'll see you and your pet soon!</p>

		<div class="card w-full border border-main/20! bg-text-main! text-left shadow-sm">
			<div class="card-body gap-2">
				<div>
					<p class="text-xs text-main/50!">Service</p>
					<p class="font-medium text-main!">{form?.appointment?.service_name}</p>
				</div>
				<div>
					<p class="text-xs text-main/50!">Date</p>
					<p class="font-medium text-main!">
						{formatDate(form?.appointment?.appointment_date ?? '')}
					</p>
				</div>
				<div>
					<p class="text-xs text-main/50!">Time</p>
					<p class="font-medium text-main!">
						{formatTime(form?.appointment?.start_time ?? '')} — {formatTime(
							form?.appointment?.end_time ?? ''
						)}
					</p>
				</div>
				<div>
					<p class="text-xs text-main/50!">Status</p>
					<span class="badge bg-main! text-xs text-text-main!">Pending</span>
				</div>
			</div>
		</div>

		<a href="/profile" class="btn w-full border-none bg-main! text-text-main! hover:bg-sub!">
			Back to Profile
		</a>
		<button
			class="btn w-full border-main! text-main! btn-outline hover:bg-main! hover:text-text-main!"
			onclick={async () => {await resetBooking(); await goto('/appointment')}}
		>
			Book Another Appointment
		</button>
	</div>
{:else}
	<div class="mx-auto flex max-w-2xl flex-col gap-6 p-6">
		<h2 class="text-2xl font-bold text-main!">Book an Appointment</h2>

		{#if form?.message}
			<div class="alert bg-red-100! text-sm text-red-700!">{form.message}</div>
		{/if}

		<form
			method="POST"
			action="?/book"
			use:enhance={() => {
				return async ({ result, update }) => {
					await update({ reset: false });
					if (result.type === 'success') {
						confirmed = true;
					}
				};
			}}
			class="flex flex-col gap-6"
		>
			<!-- Step 1: Select Pet -->
			<div class="card border border-main/20! bg-text-main! shadow-sm">
				<div class="card-body gap-3">
					<h3 class="font-semibold text-main!">1. Select Pet</h3>
					<div class="grid grid-cols-2 gap-3 sm:grid-cols-3">
						{#each data.pets as pet}
							<label class="cursor-pointer">
								<input
									type="radio"
									name="pet_id"
									value={pet.id}
									class="hidden"
									onchange={() => (selectedPet = pet.id)}
									required
								/>
								<div
									class="rounded-xl border-2 p-3 text-center transition-all
                                    {selectedPet === pet.id
										? 'border-main! bg-main! text-text-main!'
										: 'border-gray-200 hover:border-main/50!'}"
								>
									<p class="mb-1 text-2xl">
										{pet.species_type === 'Dog' ? '🐶' : pet.species_type === 'Cat' ? '🐱' : '🐾'}
									</p>
									<p class="text-sm font-medium">{pet.name}</p>
									<p class="text-xs opacity-70">{pet.breed}</p>
								</div>
							</label>
						{/each}
					</div>
				</div>
			</div>

			<!-- Step 2: Select Service -->
			{#if selectedPet}
				<div class="card border border-main/20! bg-text-main! shadow-sm">
					<div class="card-body gap-3">
						<h3 class="font-semibold text-main!">2. Select Service</h3>
						<div class="grid grid-cols-1 gap-3 sm:grid-cols-2">
							{#each data.services as service}
								<label class="cursor-pointer">
									<input
										type="radio"
										name="service_id"
										value={service.id}
										class="hidden"
										onchange={() => {
											selectedService = service.id;
											selectedDate = null;
											slots = [];
											selectedSlot = null;
										}}
										required
									/>
									<div
										class="rounded-xl border-2 p-4 transition-all
                                    {selectedService === service.id
											? 'border-main! bg-main! text-text-main!'
											: 'border-gray-200 hover:border-main/50!'}"
									>
										<p class="text-sm font-medium">{service.name}</p>
										<p class="text-xs opacity-70">
											{service.duration_mins} mins · {service.staff_type}
										</p>
									</div>
								</label>
							{/each}
						</div>
					</div>
				</div>
			{/if}

			<!-- Step 3: Pick Date -->
			{#if selectedService}
				<div class="card border border-main/20! bg-text-main! shadow-sm">
					<div class="card-body gap-3">
						<h3 class="font-semibold text-main!">3. Pick a Date</h3>
						<input
							type="date"
							name="appointment_date"
							min={minDate}
							class="input-bordered bg-slate-100 input w-full border-main! focus:outline-main!"
							onchange={async (e) => {
								selectedDate = (e.target as HTMLInputElement).value;
								await fetchSlots();
							}}
							required
						/>
					</div>
				</div>
			{/if}

			<!-- Step 4: Pick Slot -->
			{#if selectedDate}
				<div class="card border border-main/20! bg-text-main! shadow-sm">
					<div class="card-body gap-3">
						<h3 class="font-semibold text-main!">4. Pick a Time Slot</h3>

						{#if loadingSlots}
							<p class="text-sm text-main/50!">Loading available slots...</p>
						{:else if slots.length === 0}
							<p class="text-sm text-red-500!">
								No available slots for this date. Try another day.
							</p>
						{:else}
							<div class="grid grid-cols-3 gap-2 sm:grid-cols-4">
								{#each slots as slot}
									<label class="cursor-pointer">
										<input
											type="radio"
											name="start_time"
											value={slot.start_time}
											class="hidden"
											onchange={() => (selectedSlot = slot)}
											required
										/>
										<div
											class="rounded-lg border-2 p-2 text-center text-sm transition-all
                                        {selectedSlot?.start_time === slot.start_time
												? 'border-main! bg-main! text-text-main!'
												: 'border-gray-200 hover:border-main/50!'}"
										>
											{formatTime(slot.start_time)}
										</div>
									</label>
								{/each}
							</div>
						{/if}
					</div>
				</div>
			{/if}

			<!-- Step 5: Details -->
			{#if selectedSlot}
				<div class="card border border-main/20! bg-text-main! shadow-sm">
					<div class="card-body gap-3">
						<h3 class="font-semibold text-main!">5. Appointment Details</h3>

						<!-- hidden end_time -->
						<input type="hidden" name="end_time" value={selectedSlot.end_time} />

						<label class="form-control w-full">
							<div class="label">
								<span class="label-text font-medium text-main!">Visit Type</span>
							</div>
							<select
								name="visit_type_code"
								class="select-bordered bg-slate-100 select w-full border-main! focus:outline-main!"
								required
							>
								<option value="" disabled selected>Select visit type</option>
								<option value="OPD">Out-Patient (OPD)</option>
								<option value="FOLLOW_UP">Follow-up</option>
								<option value="EMERGENCY">Emergency</option>
							</select>
						</label>

						<label class="form-control w-full">
							<div class="label">
								<span class="label-text font-medium text-main!">Chief Complaint</span>
							</div>
							<textarea
								name="chief_complaint"
								class="textarea-bordered bg-slate-100 textarea w-full border-main! focus:outline-main!"
								placeholder="Describe your pet's concern..."
								rows="3"
								required
							></textarea>
						</label>

						<button
							type="submit"
							class="btn mt-2 w-full border-none bg-main! text-text-main! hover:bg-sub!"
						>
							Confirm Booking
						</button>
					</div>
				</div>
			{/if}
		</form>
	</div>
{/if}
