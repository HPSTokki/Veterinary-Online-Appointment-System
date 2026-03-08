<script lang="ts">
	import { enhance } from '$app/forms';
	import AppointmentList from './components/AppointmentList.svelte';
	let { data, form } = $props();
	let editing = $state(false);
	let addingPet = $state(false);
	let isNew = $derived(!data.profile);
	let editingPet = $state<number | null>(null);
	let deletingPet = $state<number | null>(null);
</script>

<!-- ===== FIRST TIME: Profile Creation Modal ===== -->
{#if isNew}
	<div class="fixed inset-0 z-50 flex items-center justify-center bg-black/60">
		<div class="w-full max-w-lg rounded-2xl bg-text-main p-6 shadow-2xl">
			<h2 class="mb-1 text-xl font-bold text-main!">Complete Your Profile</h2>
			<p class="mb-4 text-sm text-gray-500">Required before booking an appointment.</p>

			{#if form?.message}
				<div class="mb-3 alert bg-red-100! text-sm text-red-700!">{form.message}</div>
			{/if}

			<form method="POST" action="?/create_profile" use:enhance class="flex flex-col gap-3">
				<label class="form-control w-full">
					<div class="label"><span class="label-text font-medium text-main!">Full Name</span></div>
					<input
						type="text"
						name="full_name"
						class="input-bordered bg-text-main input w-full border-main! focus:outline-main!"
						placeholder="Juan Dela Cruz"
						required
					/>
				</label>

				<label class="form-control w-full">
					<div class="label"><span class="label-text font-medium text-main!">Address</span></div>
					<input
						type="text"
						name="address"
						class="input-bordered bg-text-main border-main1 input w-full focus:outline-main!"
						placeholder="123 Mabini St., Bulacan"
						required
					/>
				</label>

				<div class="grid grid-cols-2 gap-3">
					<label class="form-control w-full">
						<div class="label">
							<span class="label-text font-medium text-main!">Mobile No.</span>
						</div>
						<input
							type="tel"
							name="mobile_no"
							class="input-bordered bg-text-main input w-full border-main! focus:outline-main!"
							placeholder="09XX XXX XXXX"
						/>
					</label>
					<label class="form-control w-full">
						<div class="label">
							<span class="label-text font-medium text-main!">Telephone No.</span>
						</div>
						<input
							type="tel"
							name="tel_no"
							class="input-bordered bg-text-main input w-full border-main! focus:outline-main!"
							placeholder="(044) XXX XXXX"
						/>
					</label>
				</div>

				<label class="form-control w-full">
					<div class="label">
						<span class="label-text font-medium text-main!">Preferred Contact</span>
					</div>
					<select
						name="preferred_contact_method"
						class="select-bordered bg-text-main select w-full border-main! focus:outline-main!"
					>
						<option value="Mobile No.">Mobile No.</option>
						<option value="Telephone No.">Telephone No.</option>
						<option value="Email">Email</option>
					</select>
				</label>

				<button
					type="submit"
					class="btn mt-2 w-full border-none bg-main! text-text-main! hover:bg-sub!"
				>
					Save & Continue
				</button>
			</form>
		</div>
	</div>
{:else}
	<!-- ===== EXISTING PROFILE ===== -->
	<div class="mx-auto flex max-w-3xl flex-col gap-8 p-6">
		<!-- Profile Section -->
		<div>
			<div class="mb-4 flex items-center justify-between">
				<h2 class="text-2xl font-bold text-main!">My Profile</h2>
				<button
					class="btn border-main! text-main! btn-outline btn-sm hover:bg-main! hover:text-text-main!"
					onclick={() => (editing = !editing)}
				>
					{editing ? 'Cancel' : 'Edit'}
				</button>
			</div>

			{#if form?.message}
				<div class="mb-4 alert bg-red-100! text-sm text-red-700!">{form.message}</div>
			{/if}

			{#if !editing}
				<div class="card border border-main/20! bg-text-main! shadow-sm">
					<div class="card-body grid grid-cols-2 gap-4">
						{#each [{ label: 'Full Name', value: data.profile.full_name }, { label: 'Email', value: data.profile.email }, { label: 'Mobile No.', value: data.profile.mobile_no ?? '—' }, { label: 'Telephone No.', value: data.profile.tel_no ?? '—' }, { label: 'Preferred Contact', value: data.profile.preferred_contact_method }, { label: 'Address', value: data.profile.address }] as field}
							<div>
								<p class="text-xs text-main/60!">{field.label}</p>
								<p class="font-medium text-main!">{field.value}</p>
							</div>
						{/each}
					</div>
				</div>
			{:else}
				<form
					method="POST"
					action="?/update_profile"
					use:enhance
					class="card border border-main/20! bg-text-main! shadow-sm"
				>
					<div class="card-body flex flex-col gap-3">
						<label class="form-control w-full">
							<div class="label">
								<span class="label-text font-medium text-main!">Address</span>
							</div>
							<input
								type="text"
								name="address"
								class="input-bordered input w-full border-main! bg-text-main focus:outline-main!"
								value={data.profile.address}
							/>
						</label>
						<div class="grid grid-cols-2 gap-3">
							<label class="form-control w-full">
								<div class="label">
									<span class="label-text font-medium text-main!">Mobile No.</span>
								</div>
								<input
									type="tel"
									name="mobile_no"
									class="input-bordered input w-full border-main! bg-text-main focus:outline-main!"
									value={data.profile.mobile_no ?? ''}
								/>
							</label>
							<label class="form-control w-full">
								<div class="label">
									<span class="label-text font-medium text-main!">Telephone No.</span>
								</div>
								<input
									type="tel"
									name="tel_no"
									class="input-bordered input w-full border-main! bg-text-main focus:outline-main!"
									value={data.profile.tel_no ?? ''}
								/>
							</label>
						</div>
						<label class="form-control w-full">
							<div class="label">
								<span class="label-text font-medium text-main!">Preferred Contact</span>
							</div>
							<select
								name="preferred_contact_method"
								class="select-bordered select w-full border-main! bg-text-main focus:outline-main!"
							>
								<option
									value="Mobile No."
									selected={data.profile.preferred_contact_method === 'Mobile No.'}
									>Mobile No.</option
								>
								<option
									value="Telephone No."
									selected={data.profile.preferred_contact_method === 'Telephone No.'}
									>Telephone No.</option
								>
								<option value="Email" selected={data.profile.preferred_contact_method === 'Email'}
									>Email</option
								>
							</select>
						</label>
						<button
							type="submit"
							class="btn w-full border-none bg-main! text-text-main! hover:bg-sub!"
						>
							Update Profile
						</button>
					</div>
				</form>
			{/if}
		</div>

		<!-- Pets Section -->
		<div>
			<div class="mb-4 flex items-center justify-between">
				<h2 class="text-2xl font-bold text-main!">My Pets</h2>
				<button
					class="btn border-none bg-main! text-text-main! btn-sm hover:bg-sub!"
					onclick={() => (addingPet = !addingPet)}
				>
					{addingPet ? 'Cancel' : '+ Add Pet'}
				</button>
			</div>

			{#if addingPet}
				<form
					method="POST"
					action="?/add_pet"
					use:enhance={() => {
						return async ({ result, update }) => {
							await update();
							if (result.type === 'redirect' || result.type === 'success') {
								addingPet = false;
							}
						};
					}}
					class="card mb-4 border border-main/20! bg-text-main! shadow-sm"
				>
					<div class="card-body flex flex-col gap-3">
						<h3 class="text-lg font-semibold text-main!">New Pet</h3>

						<div class="grid grid-cols-2 gap-3">
							<label class="form-control w-full">
								<div class="label">
									<span class="label-text font-medium text-main!">Pet Name</span>
								</div>
								<input
									type="text"
									name="name"
									class="input-bordered input w-full border-main! bg-text-main focus:outline-main!"
									placeholder="Buddy"
									required
								/>
							</label>
							<label class="form-control w-full">
								<div class="label">
									<span class="label-text font-medium text-main!">Species</span>
								</div>
								<select
									name="species_type"
									class="select-bordered select w-full border-main! bg-text-main focus:outline-main!"
									required
								>
									<option value="" disabled selected>Select</option>
									<option value="Dog">Dog</option>
									<option value="Cat">Cat</option>
									<option value="Other">Other</option>
								</select>
							</label>
							<label class="form-control w-full">
								<div class="label">
									<span class="label-text font-medium text-main!">Breed</span>
								</div>
								<input
									type="text"
									name="breed"
									class="input-bordered input w-full border-main! bg-text-main focus:outline-main!"
									placeholder="Labrador"
									required
								/>
							</label>
							<label class="form-control w-full">
								<div class="label"><span class="label-text font-medium text-main!">Sex</span></div>
								<select
									name="sex"
									class="select-bordered select w-full border-main! bg-text-main focus:outline-main!"
									required
								>
									<option value="" disabled selected>Select</option>
									<option value="Male">Male</option>
									<option value="Female">Female</option>
								</select>
							</label>
							<label class="form-control w-full">
								<div class="label">
									<span class="label-text font-medium text-main!">Date of Birth</span>
								</div>
								<input
									type="date"
									name="date_of_birth"
									class="input-bordered input w-full border-main! bg-text-main focus:outline-main!"
									required
								/>
							</label>
							<label class="form-control w-full">
								<div class="label">
									<span class="label-text  font-medium text-main!">Weight (kg)</span>
								</div>
								<input
									type="number"
									name="weight_kg"
									class="input-bordered input w-full border-main! bg-text-main focus:outline-main!"
									placeholder="4.5"
									step="0.1"
									min="0"
								/>
							</label>
						</div>

						<label class="flex cursor-pointer items-center gap-2">
							<input
								type="checkbox"
								name="is_spayed_neutered"
								value="true"
								class="checkbox border-main! checkbox-sm checked:bg-main!"
							/>
							<span class="label-text text-main!">Spayed / Neutered</span>
						</label>

						<button
							type="submit"
							class="btn w-full border-none bg-main! text-text-main! hover:bg-sub!"
						>
							Add Pet
						</button>
					</div>
				</form>
			{/if}

			{#if data.pets.length === 0}
				<div class="py-8 text-center">
					<p class="mb-2 text-4xl">🐾</p>
					<p class="text-sm text-main/60!">No pets added yet. Add your first pet above.</p>
				</div>
			{:else}
				<div class="grid grid-cols-1 gap-4 sm:grid-cols-2">
					{#each data.pets as pet}
						<div
							class="card border border-main/20! bg-text-main! shadow-sm transition-shadow hover:shadow-md"
						>
							<div class="card-body gap-1">
								<div class="flex items-center justify-between">
									<h3 class="card-title text-base text-main!">{pet.name}</h3>
									<span class="badge badge-outline border-main! text-xs text-main!"
										>{pet.species_type}</span
									>
								</div>
								<p class="text-sm text-main/70!">{pet.breed} · {pet.sex}</p>
								<p class="text-xs text-main/50!">
									Born: {new Date(pet.date_of_birth).toLocaleDateString()}
								</p>
								{#if pet.weight_kg}
									<p class="text-xs text-main/50!">Weight: {pet.weight_kg} kg</p>
								{/if}
								<p class="text-xs text-main/50!">
									{pet.is_spayed_neutered ? '✓ Spayed/Neutered' : '✗ Not Spayed/Neutered'}
								</p>

								<!-- Edit inline form -->
								{#if editingPet === pet.id}
									<form
										method="POST"
										action="?/edit_pet"
										use:enhance={() => {
											return async ({ result, update }) => {
												await update();
												if (result.type === 'redirect') editingPet = null;
											};
										}}
										class="mt-2 flex flex-col gap-2 border-t border-main/20! pt-2"
									>
										<input type="hidden" name="pet_id" value={pet.id} />
										<label class="form-control w-full">
											<div class="label">
												<span class="label-text text-xs text-main!">Weight (kg)</span>
											</div>
											<input
												type="number"
												name="weight_kg"
												step="0.1"
												min="0"
												class="input-bordered bg-text-main input input-sm w-full border-main!"
												value={pet.weight_kg ?? ''}
											/>
										</label>
										<label class="flex cursor-pointer items-center gap-2">
											<input
												type="checkbox"
												name="is_spayed_neutered"
												value="true"
												class="checkbox border-main! checkbox-sm checked:bg-main!"
												checked={pet.is_spayed_neutered}
											/>
											<span class="label-text text-xs text-main!">Spayed / Neutered</span>
										</label>
										<div class="flex gap-2">
											<button
												type="button"
												class="btn flex-1 border-main! text-main! btn-outline btn-xs"
												onclick={() => (editingPet = null)}>Cancel</button
											>
											<button
												type="submit"
												class="btn flex-1 border-none bg-main! text-text-main! btn-xs">Save</button
											>
										</div>
									</form>
								{:else}
									<div class="mt-2 flex gap-2">
										<button
											class="btn flex-1 border-main! text-main! btn-outline btn-xs hover:bg-main! hover:text-text-main!"
											onclick={() => (editingPet = pet.id)}
										>
											Edit
										</button>
										<button
											class="btn flex-1 border-red-400! text-red-400! btn-outline btn-xs hover:bg-red-400! hover:text-white!"
											onclick={() => (deletingPet = pet.id)}
										>
											Delete
										</button>
									</div>
								{/if}
							</div>
						</div>
					{/each}

					<!-- Delete Confirm Dialog -->
					{#if deletingPet}
						<div
							class="fixed inset-0 z-50 flex items-center justify-center bg-black/50"
							role="dialog"
							aria-modal="true"
						>
							<div class="w-full max-w-sm rounded-2xl bg-text-main! p-6 shadow-2xl">
								<h3 class="mb-2 text-lg font-bold text-main!">Delete Pet?</h3>
								<p class="mb-4 text-sm text-main/60!">
									This cannot be undone. Make sure there are no active appointments for this pet.
								</p>
								<div class="flex gap-2">
									<button
										class="btn flex-1 border-main! text-main! btn-outline"
										onclick={() => (deletingPet = null)}
									>
										Cancel
									</button>
									<form method="POST" action="?/delete_pet" use:enhance class="flex-1">
										<input type="hidden" name="pet_id" value={deletingPet} />
										<button
											type="submit"
											class="btn w-full border-none bg-red-400! text-white! hover:bg-red-500!"
										>
											Delete
										</button>
									</form>
								</div>
							</div>
						</div>
					{/if}
				</div>
			{/if}
		</div>
		<!-- Appointments -->
		<div>
			<div class="mb-4 flex items-center justify-between">
				<h2 class="text-2xl font-bold text-main!">My Appointments</h2>
				<a href="/book" class="btn-main! bg-main! btn border-none text-text-main! btn-sm hover:bg-sub!"
					>+ Book Appointment</a
				>
			</div>
			<AppointmentList appointments={data.appointments} />
		</div>
	</div>
{/if}
