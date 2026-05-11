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
		XCircle,
		CalendarDays,
		Clock,
		Ban,
		TrendingUp
	} from '@lucide/svelte';
	import AppointmentList from './components/AppointmentList.svelte';

	let { data, form } = $props();
	let editing = $state(false);
	let addingPet = $state(false);
	let isNew = $derived(!data.profile);
	let editingPet = $state<number | null>(null);
	let deletingPet = $state<number | null>(null);

	const inp =
		'input w-full border-transparent bg-slate-100 text-main placeholder:text-main/30 focus:border-main focus:outline-none transition-colors';
	const sel =
		'select w-full border-transparent bg-slate-100 text-main focus:border-main focus:outline-none transition-colors';
	const lbl = 'label-text font-medium text-slate-500';

	// Derived appointment buckets
	const upcoming = $derived(
		(data.appointments ?? []).filter((a: any) => ['pending', 'confirmed'].includes(a.status))
	);
	const cancelled = $derived(
		(data.appointments ?? []).filter((a: any) => a.status === 'cancelled')
	);

	function formatDate(dt: string) {
		return new Date(dt).toLocaleDateString([], {
			weekday: 'short',
			month: 'short',
			day: 'numeric'
		});
	}
	function formatTime(dt: string) {
		return new Date(dt).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
	}

	const visitLabels: Record<string, string> = {
		OPD: 'Out-Patient',
		FOLLOW_UP: 'Follow-up',
		EMERGENCY: 'Emergency'
	};
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
	<!-- ===== DASHBOARD LAYOUT ===== -->
	<div class="min-h-screen bg-slate-50 p-4 sm:p-6">
		<!-- Page header -->
		<div class="mb-6 flex items-center justify-between">
			<div>
				<h1 class="text-2xl font-bold text-main sm:text-3xl">My Dashboard</h1>
				<p class="text-sm text-slate-500">Welcome back, {data.profile.full_name.split(' ')[0]}</p>
			</div>
			<a href="/book" class="btn gap-2 border-none bg-main text-text-main hover:bg-sub">
				<CalendarPlus size={16} /> Book Appointment
			</a>
		</div>

		<!-- ── 3-column grid (stacks on mobile) ── -->
		<div class="grid grid-cols-1 gap-6 lg:grid-cols-3">
			<!-- ════ COL 1: Profile + Pets ════ -->
			<div class="flex flex-col gap-6">
				<!-- Profile card -->
				<div class="card bg-white shadow-sm">
					<div class="card-body gap-3 p-5">
						<div class="flex items-center justify-between">
							<div class="flex items-center gap-2">
								<User size={16} class="text-main/60" />
								<h2 class="font-bold text-main">Profile</h2>
							</div>
							<button
								class="btn border-main text-main btn-outline btn-xs hover:bg-main hover:text-text-main"
								onclick={() => (editing = !editing)}
							>
								{#if editing}<X size={12} />Cancel{:else}<Pencil size={12} />Edit{/if}
							</button>
						</div>

						{#if form?.message}
							<div class="alert py-2 text-xs alert-error" transition:slide={{ duration: 200 }}>
								{form.message}
							</div>
						{/if}

						{#if !editing}
							<div class="flex flex-col gap-2" transition:fade={{ duration: 150 }}>
								{#each [{ icon: User, label: 'Name', value: data.profile.full_name }, { icon: Mail, label: 'Email', value: data.profile.email }, { icon: Phone, label: 'Mobile', value: data.profile.mobile_no ?? '—' }, { icon: PhoneCall, label: 'Tel', value: data.profile.tel_no ?? '—' }, { icon: MapPin, label: 'Address', value: data.profile.address }] as f (f.label)}
									<div class="flex items-start gap-2">
										<svelte:component
											this={f.icon}
											size={13}
											class="mt-0.5 shrink-0 text-main/30"
										/>
										<div class="min-w-0">
											<p class="text-xs text-slate-400">{f.label}</p>
											<p class="truncate text-sm font-medium text-main">{f.value}</p>
										</div>
									</div>
								{/each}
							</div>
						{:else}
							<form
								method="POST"
								action="?/update_profile"
								use:enhance
								class="flex flex-col gap-2"
								transition:fly={{ y: 6, duration: 200, easing: cubicOut }}
							>
								<label class="form-control w-full">
									<div class="label pb-1"><span class="{lbl} text-xs">Address</span></div>
									<input type="text" name="address" class={inp} value={data.profile.address} />
								</label>
								<div class="grid grid-cols-2 gap-2">
									<label class="form-control w-full">
										<div class="label pb-1"><span class="{lbl} text-xs">Mobile</span></div>
										<input
											type="tel"
											name="mobile_no"
											class={inp}
											value={data.profile.mobile_no ?? ''}
										/>
									</label>
									<label class="form-control w-full">
										<div class="label pb-1"><span class="{lbl} text-xs">Tel</span></div>
										<input type="tel" name="tel_no" class={inp} value={data.profile.tel_no ?? ''} />
									</label>
								</div>
								<label class="form-control w-full">
									<div class="label pb-1"><span class="{lbl} text-xs">Preferred Contact</span></div>
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
										<option
											value="Email"
											selected={data.profile.preferred_contact_method === 'Email'}>Email</option
										>
									</select>
								</label>
								<button
									type="submit"
									class="btn mt-1 w-full border-none bg-main text-text-main btn-sm hover:bg-sub"
								>
									Save
								</button>
							</form>
						{/if}
					</div>
				</div>

				<!-- Pets card -->
				<div class="card bg-white shadow-sm">
					<div class="card-body gap-3 p-5">
						<div class="flex items-center justify-between">
							<div class="flex items-center gap-2">
								<PawPrint size={16} class="text-main/60" />
								<h2 class="font-bold text-main">My Pets</h2>
							</div>
							<button
								class="btn border-none bg-main text-text-main btn-xs hover:bg-sub"
								onclick={() => (addingPet = !addingPet)}
							>
								{#if addingPet}<X size={12} />Cancel{:else}<Plus size={12} />Add{/if}
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
								class="flex flex-col gap-2 border-t border-slate-100 pt-3"
								transition:slide={{ duration: 250 }}
							>
								<div class="grid grid-cols-2 gap-2">
									<label class="form-control w-full">
										<div class="label pb-1"><span class="{lbl} text-xs">Name</span></div>
										<input type="text" name="name" class={inp} placeholder="Buddy" required />
									</label>
									<label class="form-control w-full">
										<div class="label pb-1"><span class="{lbl} text-xs">Species</span></div>
										<select name="species_type" class={sel} required>
											<option value="" disabled selected>Select</option>
											<option value="Dog">Dog</option>
											<option value="Cat">Cat</option>
											<option value="Other">Other</option>
										</select>
									</label>
									<label class="form-control w-full">
										<div class="label pb-1"><span class="{lbl} text-xs">Breed</span></div>
										<input type="text" name="breed" class={inp} placeholder="Labrador" required />
									</label>
									<label class="form-control w-full">
										<div class="label pb-1"><span class="{lbl} text-xs">Sex</span></div>
										<select name="sex" class={sel} required>
											<option value="" disabled selected>Select</option>
											<option value="Male">Male</option>
											<option value="Female">Female</option>
										</select>
									</label>
									<label class="form-control w-full">
										<div class="label pb-1"><span class="{lbl} text-xs">Date of Birth</span></div>
										<input type="date" name="date_of_birth" class={inp} required />
									</label>
									<label class="form-control w-full">
										<div class="label pb-1"><span class="{lbl} text-xs">Weight (kg)</span></div>
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
									<span class="label-text text-xs text-slate-500">Spayed / Neutered</span>
								</label>
								<button
									type="submit"
									class="btn w-full border-none bg-main text-text-main btn-sm hover:bg-sub"
								>
									Add Pet
								</button>
							</form>
						{/if}

						{#if data.pets.length === 0 && !addingPet}
							<div class="flex flex-col items-center gap-1 py-6 text-center">
								<PawPrint size={28} class="text-main/20" />
								<p class="text-xs text-slate-400">No pets yet.</p>
							</div>
						{:else}
							<div class="flex flex-col gap-2">
								{#each data.pets as pet (pet.id)}
									<div class="rounded-xl border border-slate-100 bg-slate-50 p-3">
										<div class="flex items-center justify-between">
											<div>
												<div class="flex items-center gap-1.5">
													<PawPrint size={13} class="text-main/50" />
													<span class="text-sm font-semibold text-main">{pet.name}</span>
													<span class="badge badge-outline border-main/20 text-xs text-main/60"
														>{pet.species_type}</span
													>
												</div>
												<p class="mt-0.5 text-xs text-slate-400">{pet.breed} · {pet.sex}</p>
												<div class="mt-1 flex flex-wrap gap-x-3 gap-y-0.5">
													<span class="text-xs text-slate-400"
														>Born {new Date(pet.date_of_birth).toLocaleDateString()}</span
													>
													{#if pet.weight_kg}
														<span class="flex items-center gap-0.5 text-xs text-slate-400">
															<Weight size={10} />{pet.weight_kg}kg
														</span>
													{/if}
													<span
														class="flex items-center gap-0.5 text-xs {pet.is_spayed_neutered
															? 'text-main'
															: 'text-slate-400'}"
													>
														{#if pet.is_spayed_neutered}<CheckCircle
																size={10}
															/>Spayed{:else}<XCircle size={10} />Not spayed{/if}
													</span>
												</div>
											</div>
										</div>

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
												class="mt-2 flex flex-col gap-2 border-t border-slate-200 pt-2"
												transition:slide={{ duration: 200 }}
											>
												<input type="hidden" name="pet_id" value={pet.id} />
												<label class="form-control w-full">
													<div class="label pb-1">
														<span class="{lbl} text-xs">Weight (kg)</span>
													</div>
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
														class="btn flex-1 border-none bg-main text-text-main btn-xs"
														>Save</button
													>
												</div>
											</form>
										{:else}
											<div class="mt-2 flex gap-1.5" transition:fade={{ duration: 150 }}>
												<button
													class="btn flex-1 border-main text-main btn-outline btn-xs hover:bg-main hover:text-text-main"
													onclick={() => (editingPet = pet.id)}
												>
													<Pencil size={11} /> Edit
												</button>
												<button
													class="btn flex-1 border-red-300 text-red-400 btn-outline btn-xs hover:bg-red-400 hover:text-white"
													onclick={() => (deletingPet = pet.id)}
												>
													<Trash2 size={11} /> Delete
												</button>
											</div>
										{/if}
									</div>
								{/each}
							</div>
						{/if}
					</div>
				</div>
			</div>
			<!-- END COL 1 -->

			<!-- ════ COL 2: Appointments (upcoming + cancelled) ════ -->
			<div class="flex flex-col gap-6">
				<!-- Upcoming -->
				<div class="card bg-white shadow-sm">
					<div class="card-body gap-3 p-5">
						<div class="flex items-center gap-2">
							<CalendarDays size={16} class="text-main/60" />
							<h2 class="font-bold text-main">Upcoming</h2>
							{#if upcoming.length > 0}
								<span class="badge border-none bg-main/10 badge-sm text-main"
									>{upcoming.length}</span
								>
							{/if}
						</div>

						{#if upcoming.length === 0}
							<div class="flex flex-col items-center gap-1 py-6 text-center">
								<CalendarDays size={28} class="text-main/20" />
								<p class="text-xs text-slate-400">No upcoming appointments.</p>
							</div>
						{:else}
							<AppointmentList appointments={upcoming} token={data.token ?? ''} />
						{/if}
					</div>
				</div>

				<!-- Cancelled -->
				{#if cancelled.length > 0}
					<div class="card bg-white shadow-sm">
						<div class="card-body gap-3 p-5">
							<div class="flex items-center gap-2">
								<Ban size={16} class="text-slate-400" />
								<h2 class="font-bold text-slate-500">Cancelled</h2>
								<span class="badge border-none bg-slate-100 badge-sm text-slate-400"
									>{cancelled.length}</span
								>
							</div>
							<div class="flex flex-col gap-2">
								{#each cancelled as appt (appt.id)}
									<div class="rounded-xl bg-slate-50 p-3 opacity-70">
										<div class="flex items-center justify-between">
											<p class="text-sm font-medium text-slate-500">{appt.service_name}</p>
											<span class="badge border-none bg-slate-200 badge-sm text-slate-400"
												>cancelled</span
											>
										</div>
										<div class="mt-1 flex items-center gap-3 text-xs text-slate-400">
											<span class="flex items-center gap-1"
												><CalendarDays size={10} />{formatDate(appt.appointment_date)}</span
											>
											<span class="flex items-center gap-1"
												><Clock size={10} />{formatTime(appt.start_time)}</span
											>
											<span class="flex items-center gap-1"
												><PawPrint size={10} />{appt.pet_name}</span
											>
										</div>
									</div>
								{/each}
							</div>
						</div>
					</div>
				{/if}
			</div>
			<!-- END COL 2 -->

			<!-- ════ COL 3: Quick stats ════ -->
			<div class="flex flex-col gap-6">
				<div class="card bg-white shadow-sm">
					<div class="card-body gap-4 p-5">
						<div class="flex items-center gap-2">
							<TrendingUp size={16} class="text-main/60" />
							<h2 class="font-bold text-main">Overview</h2>
						</div>

						<div class="grid grid-cols-2 gap-3">
							{#each [{ label: 'Pets', value: data.pets.length, icon: PawPrint, color: 'bg-main/10 text-main' }, { label: 'Upcoming', value: upcoming.length, icon: CalendarDays, color: 'bg-emerald-50 text-emerald-600' }, { label: 'Cancelled', value: cancelled.length, icon: Ban, color: 'bg-slate-100 text-slate-500' }] as stat (stat.label)}
								<div class="flex flex-col gap-1 rounded-xl {stat.color} p-3">
									<svelte:component this={stat.icon} size={16} />
									<p class="text-2xl font-bold">{stat.value}</p>
									<p class="text-xs opacity-70">{stat.label}</p>
								</div>
							{/each}
						</div>

						<!-- Client since -->
						<div class="rounded-xl bg-slate-50 px-4 py-3">
							<p class="text-xs text-slate-400">Client since</p>
							<p class="font-semibold text-main">
								{new Date(data.profile.created_at).toLocaleDateString([], {
									year: 'numeric',
									month: 'long'
								})}
							</p>
						</div>

						<!-- Next appointment teaser -->
						{#if upcoming.length > 0}
							{@const next = upcoming.sort(
								(a: any, b: any) =>
									new Date(a.appointment_date).getTime() - new Date(b.appointment_date).getTime()
							)[0]}
							<div class="rounded-xl border border-main/20 bg-main/5 px-4 py-3">
								<p class="mb-1 text-xs font-medium tracking-wide text-main/60 uppercase">
									Next Appointment
								</p>
								<p class="font-semibold text-main">{next.service_name}</p>
								<p class="mt-0.5 text-xs text-slate-500">
									{formatDate(next.appointment_date)} · {formatTime(next.start_time)}
								</p>
								<p class="mt-0.5 flex items-center gap-1 text-xs text-slate-400">
									<PawPrint size={10} />{next.pet_name}
								</p>
							</div>
						{/if}
					</div>
				</div>
			</div>
			<!-- END COL 3 -->
		</div>
	</div>

	<!-- Delete Pet Confirm Dialog -->
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
								class="btn w-full border-none bg-red-400 text-white hover:bg-red-500">Delete</button
							>
						</form>
					</div>
				</div>
			</div>
		</div>
	{/if}
{/if}
