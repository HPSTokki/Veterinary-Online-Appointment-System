<script lang="ts">
	import { enhance } from '$app/forms';
	import { fly, fade, slide } from 'svelte/transition';
	import { cubicOut } from 'svelte/easing';
	import {
		User,
		MapPin,
		Phone,
		PhoneCall,
		Mail,
		PawPrint,
		Plus,
		Pencil,
		Trash2,
		X,
		CalendarPlus,
		Weight,
		CheckCircle,
		XCircle
	} from '@lucide/svelte';
	import AppointmentList from './components/AppointmentList.svelte';

	let { data, form } = $props();
	let editing = $state(false);
	let addingPet = $state(false);
	let isNew = $derived(!data.profile);
	let editingPet = $state<number | null>(null);
	let deletingPet = $state<number | null>(null);

	// Shared input/label classes
	const inp =
		'input w-full border-transparent bg-slate-100 text-main placeholder:text-main/30 focus:border-main focus:outline-none transition-colors';
	const sel =
		'select w-full border-transparent bg-slate-100 text-main focus:border-main focus:outline-none transition-colors';
	const lbl = 'label-text font-medium text-slate-500';
</script>

<!-- ===== FIRST TIME: Profile Creation Modal ===== -->
{#if isNew}
	<div
		class="fixed inset-0 z-50 flex items-center justify-center bg-black/60 p-4"
		transition:fade={{ duration: 200 }}
	>
		<div
			class="w-full max-w-lg overflow-hidden rounded-2xl bg-white shadow-2xl"
			transition:fly={{ y: 24, duration: 300, easing: cubicOut }}
		>
			<div class="bg-main px-6 py-5">
				<h2 class="text-xl font-bold text-text-main">Complete Your Profile</h2>
				<p class="mt-0.5 text-xs text-text-main/70">Required before booking an appointment.</p>
			</div>

			<div class="p-6">
				{#if form?.message}
					<div class="mb-4 alert py-2 text-sm alert-error" transition:slide={{ duration: 200 }}>
						{form.message}
					</div>
				{/if}

				<form method="POST" action="?/create_profile" use:enhance class="flex flex-col gap-3">
					<label class="form-control w-full">
						<div class="label pb-1"><span class={lbl}>Full Name</span></div>
						<input type="text" name="full_name" class={inp} placeholder="Juan Dela Cruz" required />
					</label>

					<label class="form-control w-full">
						<div class="label pb-1"><span class={lbl}>Address</span></div>
						<input
							type="text"
							name="address"
							class={inp}
							placeholder="123 Mabini St., Bulacan"
							required
						/>
					</label>

					<div class="grid grid-cols-2 gap-3">
						<label class="form-control w-full">
							<div class="label pb-1"><span class={lbl}>Mobile No.</span></div>
							<input type="tel" name="mobile_no" class={inp} placeholder="09XX XXX XXXX" />
						</label>
						<label class="form-control w-full">
							<div class="label pb-1"><span class={lbl}>Telephone No.</span></div>
							<input type="tel" name="tel_no" class={inp} placeholder="(044) XXX XXXX" />
						</label>
					</div>

					<label class="form-control w-full">
						<div class="label pb-1"><span class={lbl}>Preferred Contact</span></div>
						<select name="preferred_contact_method" class={sel}>
							<option value="Mobile No.">Mobile No.</option>
							<option value="Telephone No.">Telephone No.</option>
							<option value="Email">Email</option>
						</select>
					</label>

					<button
						type="submit"
						class="btn mt-2 w-full border-none bg-main text-text-main hover:bg-sub"
					>
						Save & Continue
					</button>
				</form>
			</div>
		</div>
	</div>
{:else}
	<!-- ===== EXISTING PROFILE ===== -->
	<div class="mx-auto flex max-w-3xl flex-col gap-8 p-4 sm:p-6">
		<!-- ── Profile Section ── -->
		<section>
			<div class="mb-4 flex items-center justify-between">
				<div class="flex items-center gap-2">
					<User size={20} class="text-main" />
					<h2 class="text-2xl font-bold text-main">My Profile</h2>
				</div>
				<button
					class="btn border-main text-main btn-outline btn-sm hover:bg-main hover:text-text-main"
					onclick={() => {
						editing = !editing;
					}}
				>
					{#if editing}<X size={14} class="mr-1" />Cancel{:else}<Pencil
							size={14}
							class="mr-1"
						/>Edit{/if}
				</button>
			</div>

			{#if form?.message}
				<div class="mb-4 alert py-2 text-sm alert-error" transition:slide={{ duration: 200 }}>
					{form.message}
				</div>
			{/if}

			{#if !editing}
				<div class="card bg-white shadow-sm" transition:fade={{ duration: 150 }}>
					<div class="card-body grid grid-cols-1 gap-4 sm:grid-cols-2">
						{#each [{ icon: User, label: 'Full Name', value: data.profile.full_name }, { icon: Mail, label: 'Email', value: data.profile.email }, { icon: Phone, label: 'Mobile No.', value: data.profile.mobile_no ?? '—' }, { icon: PhoneCall, label: 'Telephone No.', value: data.profile.tel_no ?? '—' }, { icon: Mail, label: 'Preferred Contact', value: data.profile.preferred_contact_method }, { icon: MapPin, label: 'Address', value: data.profile.address }] as field (field.label)}
							<div class="flex items-start gap-2">
								<svelte:component
									this={field.icon}
									size={14}
									class="mt-0.5 shrink-0 text-main/40"
								/>
								<div>
									<p class="text-xs text-slate-500">{field.label}</p>
									<p class="font-medium text-main">{field.value}</p>
								</div>
							</div>
						{/each}
					</div>
				</div>
			{:else}
				<form
					method="POST"
					action="?/update_profile"
					use:enhance
					class="card bg-white shadow-sm"
					transition:fly={{ y: 8, duration: 200, easing: cubicOut }}
				>
					<div class="card-body flex flex-col gap-3">
						<label class="form-control w-full">
							<div class="label pb-1"><span class={lbl}>Address</span></div>
							<input type="text" name="address" class={inp} value={data.profile.address} />
						</label>
						<div class="grid grid-cols-2 gap-3">
							<label class="form-control w-full">
								<div class="label pb-1"><span class={lbl}>Mobile No.</span></div>
								<input
									type="tel"
									name="mobile_no"
									class={inp}
									value={data.profile.mobile_no ?? ''}
								/>
							</label>
							<label class="form-control w-full">
								<div class="label pb-1"><span class={lbl}>Telephone No.</span></div>
								<input type="tel" name="tel_no" class={inp} value={data.profile.tel_no ?? ''} />
							</label>
						</div>
						<label class="form-control w-full">
							<div class="label pb-1"><span class={lbl}>Preferred Contact</span></div>
							<select name="preferred_contact_method" class={sel}>
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
							class="btn w-full border-none bg-main text-text-main hover:bg-sub"
						>
							Update Profile
						</button>
					</div>
				</form>
			{/if}
		</section>

		<!-- ── Pets Section ── -->
		<section>
			<div class="mb-4 flex items-center justify-between">
				<div class="flex items-center gap-2">
					<PawPrint size={20} class="text-main" />
					<h2 class="text-2xl font-bold text-main">My Pets</h2>
				</div>
				<button
					class="btn border-none bg-main text-text-main btn-sm hover:bg-sub"
					onclick={() => (addingPet = !addingPet)}
				>
					{#if addingPet}
						<X size={14} />Cancel
					{:else}
						<Plus size={14} />Add Pet
					{/if}
				</button>
			</div>

			{#if addingPet}
				<form
					method="POST"
					action="?/add_pet"
					use:enhance={() => {
						return async ({ result, update }) => {
							await update();
							if (result.type === 'redirect' || result.type === 'success') addingPet = false;
						};
					}}
					class="card mb-4 bg-white shadow-sm"
					transition:slide={{ duration: 250 }}
				>
					<div class="card-body flex flex-col gap-3">
						<h3 class="flex items-center gap-2 text-lg font-semibold text-main">
							<PawPrint size={16} /> New Pet
						</h3>

						<div class="grid grid-cols-2 gap-3">
							<label class="form-control w-full">
								<div class="label pb-1"><span class={lbl}>Pet Name</span></div>
								<input type="text" name="name" class={inp} placeholder="Buddy" required />
							</label>
							<label class="form-control w-full">
								<div class="label pb-1"><span class={lbl}>Species</span></div>
								<select name="species_type" class={sel} required>
									<option value="" disabled selected>Select</option>
									<option value="Dog">Dog</option>
									<option value="Cat">Cat</option>
									<option value="Other">Other</option>
								</select>
							</label>
							<label class="form-control w-full">
								<div class="label pb-1"><span class={lbl}>Breed</span></div>
								<input type="text" name="breed" class={inp} placeholder="Labrador" required />
							</label>
							<label class="form-control w-full">
								<div class="label pb-1"><span class={lbl}>Sex</span></div>
								<select name="sex" class={sel} required>
									<option value="" disabled selected>Select</option>
									<option value="Male">Male</option>
									<option value="Female">Female</option>
								</select>
							</label>
							<label class="form-control w-full">
								<div class="label pb-1"><span class={lbl}>Date of Birth</span></div>
								<input type="date" name="date_of_birth" class={inp} required />
							</label>
							<label class="form-control w-full">
								<div class="label pb-1"><span class={lbl}>Weight (kg)</span></div>
								<input
									type="number"
									name="weight_kg"
									class={inp}
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
								class="checkbox border-main checkbox-sm checked:bg-main"
							/>
							<span class="label-text text-slate-500">Spayed / Neutered</span>
						</label>

						<button
							type="submit"
							class="btn w-full border-none bg-main text-text-main hover:bg-sub"
						>
							Add Pet
						</button>
					</div>
				</form>
			{/if}

			{#if data.pets.length === 0}
				<div class="flex flex-col items-center gap-2 py-12 text-center">
					<PawPrint size={36} class="text-main/20" />
					<p class="text-sm text-slate-500">No pets added yet. Add your first pet above.</p>
				</div>
			{:else}
				<div class="grid grid-cols-1 gap-4 sm:grid-cols-2">
					{#each data.pets as pet (pet.id)}
						<div class="card bg-white shadow-sm transition-shadow hover:shadow-md">
							<div class="card-body gap-2">
								<!-- Pet header -->
								<div class="flex items-center justify-between">
									<div class="flex items-center gap-2">
										<PawPrint size={16} class="text-main/50" />
										<h3 class="card-title text-base text-main">{pet.name}</h3>
									</div>
									<span class="badge badge-outline border-main/30 text-xs text-main"
										>{pet.species_type}</span
									>
								</div>

								<p class="text-sm text-slate-500">{pet.breed} · {pet.sex}</p>

								<div class="flex flex-wrap gap-x-4 gap-y-1">
									<p class="flex items-center gap-1 text-xs text-slate-400">
										<CalendarPlus size={11} /> Born: {new Date(
											pet.date_of_birth
										).toLocaleDateString()}
									</p>
									{#if pet.weight_kg}
										<p class="flex items-center gap-1 text-xs text-slate-400">
											<Weight size={11} />
											{pet.weight_kg} kg
										</p>
									{/if}
									<p
										class="flex items-center gap-1 text-xs {pet.is_spayed_neutered
											? 'text-main'
											: 'text-slate-400'}"
									>
										{#if pet.is_spayed_neutered}
											<CheckCircle size={11} /> Spayed/Neutered
										{:else}
											<XCircle size={11} /> Not Spayed/Neutered
										{/if}
									</p>
								</div>

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
										class="mt-2 flex flex-col gap-2 border-t border-slate-100 pt-3"
										transition:slide={{ duration: 200 }}
									>
										<input type="hidden" name="pet_id" value={pet.id} />
										<label class="form-control w-full">
											<div class="label pb-1"><span class="{lbl} text-xs">Weight (kg)</span></div>
											<input
												type="number"
												name="weight_kg"
												step="0.1"
												min="0"
												class="input input-sm w-full border-transparent bg-slate-100 text-main focus:border-main focus:outline-none"
												value={pet.weight_kg ?? ''}
											/>
										</label>
										<label class="flex cursor-pointer items-center gap-2">
											<input
												type="checkbox"
												name="is_spayed_neutered"
												value="true"
												class="checkbox border-main checkbox-sm checked:bg-main"
												checked={pet.is_spayed_neutered}
											/>
											<span class="label-text text-xs text-slate-500">Spayed / Neutered</span>
										</label>
										<div class="flex gap-2">
											<button
												type="button"
												class="btn flex-1 border-main text-main btn-outline btn-xs"
												onclick={() => (editingPet = null)}>Cancel</button
											>
											<button
												type="submit"
												class="btn flex-1 border-none bg-main text-text-main btn-xs">Save</button
											>
										</div>
									</form>
								{:else}
									<div class="mt-2 flex gap-2" transition:fade={{ duration: 150 }}>
										<button
											class="btn flex-1 border-main text-main btn-outline btn-xs hover:bg-main hover:text-text-main"
											onclick={() => (editingPet = pet.id)}
										>
											<Pencil size={12} /> Edit
										</button>
										<button
											class="btn flex-1 border-red-400 text-red-400 btn-outline btn-xs hover:bg-red-400 hover:text-white"
											onclick={() => (deletingPet = pet.id)}
										>
											<Trash2 size={12} /> Delete
										</button>
									</div>
								{/if}
							</div>
						</div>
					{/each}
				</div>
			{/if}

			<!-- Delete Confirm Dialog -->
			{#if deletingPet}
				<div
					class="fixed inset-0 z-50 flex items-center justify-center bg-black/50 p-4"
					transition:fade={{ duration: 150 }}
				>
					<div
						class="w-full max-w-sm overflow-hidden rounded-2xl bg-white shadow-2xl"
						transition:fly={{ y: 16, duration: 250, easing: cubicOut }}
					>
						<div class="bg-red-50 px-6 py-4">
							<div class="flex items-center gap-2">
								<Trash2 size={18} class="text-red-500" />
								<h3 class="text-lg font-bold text-red-600">Delete Pet?</h3>
							</div>
						</div>
						<div class="p-6">
							<p class="mb-5 text-sm text-slate-500">
								This cannot be undone. Make sure there are no active appointments for this pet.
							</p>
							<div class="flex gap-2">
								<button
									class="btn flex-1 border-main text-main btn-outline"
									onclick={() => (deletingPet = null)}>Cancel</button
								>
								<form method="POST" action="?/delete_pet" use:enhance class="flex-1">
									<input type="hidden" name="pet_id" value={deletingPet} />
									<button
										type="submit"
										class="btn w-full border-none bg-red-400 text-white hover:bg-red-500"
										>Delete</button
									>
								</form>
							</div>
						</div>
					</div>
				</div>
			{/if}
		</section>

		<!-- ── Appointments Section ── -->
		<section>
			<div class="mb-4 flex items-center justify-between">
				<div class="flex items-center gap-2">
					<CalendarPlus size={20} class="text-main" />
					<h2 class="text-2xl font-bold text-main">My Appointments</h2>
				</div>
				<a href="/book" class="btn border-none bg-main text-text-main btn-sm hover:bg-sub">
					<Plus size={14} /> Book
				</a>
			</div>
			<AppointmentList appointments={data.appointments} token={data.token ?? ''} />
		</section>
	</div>
{/if}
