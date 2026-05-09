<script lang="ts">
	import { enhance } from '$app/forms';
	import { fly, fade, slide } from 'svelte/transition';
	import { cubicOut } from 'svelte/easing';
	import {
		CalendarDays,
		Clock,
		Stethoscope,
		PawPrint,
		X,
		Pencil,
		AlertCircle,
		LoaderCircle
	} from '@lucide/svelte';
	import { BASE_URL } from '$lib/api/auth';

	interface Appointment {
		id: number;
		service_id: number;
		pet_name: string | null;
		service_name: string | null;
		appointment_date: string;
		start_time: string;
		end_time: string;
		visit_type_code: string;
		chief_complaint: string;
		status: string;
	}

	interface Slot {
		start_time: string;
		end_time: string;
	}

	let { appointments, token }: { appointments: Appointment[]; token: string } = $props();

	let editingAppointment = $state<Appointment | null>(null);

	// Reschedule state
	let editDate = $state('');
	let slots = $state<Slot[]>([]);
	let slotsLoading = $state(false);
	let slotsError = $state<string | null>(null);
	let selectedSlot = $state<Slot | null>(null);

	// Other editable fields
	let editVisitType = $state('');
	let editComplaint = $state('');

	const active = $derived(
		appointments
			.filter((a) => ['pending', 'confirmed'].includes(a.status))
			.sort(
				(a, b) => new Date(a.appointment_date).getTime() - new Date(b.appointment_date).getTime()
			)
	);

	function formatDate(dt: string) {
		return new Date(dt).toLocaleDateString([], {
			weekday: 'short',
			year: 'numeric',
			month: 'short',
			day: 'numeric'
		});
	}
	function formatTime(dt: string) {
		return new Date(dt).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
	}
	function toDateLocal(dt: string) {
		const d = new Date(dt);
		const p = (n: number) => String(n).padStart(2, '0');
		return `${d.getFullYear()}-${p(d.getMonth() + 1)}-${p(d.getDate())}`;
	}

	const today = toDateLocal(new Date().toISOString());

	const visitLabels: Record<string, string> = {
		OPD: 'Out-Patient',
		FOLLOW_UP: 'Follow-up',
		EMERGENCY: 'Emergency'
	};

	function openEdit(appt: Appointment) {
		editingAppointment = appt;
		editDate = toDateLocal(appt.appointment_date);
		editVisitType = appt.visit_type_code;
		editComplaint = appt.chief_complaint;
		slots = [];
		selectedSlot = null;
		slotsError = null;
	}

	function closeEdit() {
		editingAppointment = null;
		slots = [];
		selectedSlot = null;
		slotsError = null;
	}

	async function fetchSlots() {
		if (!editingAppointment || !editDate) return;
		slotsLoading = true;
		slotsError = null;
		slots = [];
		selectedSlot = null;

		try {
			const res = await fetch(
				`${BASE_URL}/appointment/available-slots?service_id=${editingAppointment.service_id}&date=${editDate}T00:00:00`,
				{ headers: { Authorization: `Bearer ${token}` } }
			);
			if (!res.ok) {
				const err = await res.json();
				slotsError = err.detail ?? 'Could not load slots.';
			} else {
				slots = await res.json();
				if (slots.length === 0) slotsError = 'No available slots on this date.';
			}
		} catch {
			slotsError = 'Network error. Please try again.';
		} finally {
			slotsLoading = false;
		}
	}

	// Build the form body for the server action
	// We still post through the SvelteKit action so the server handles the API call with the httpOnly cookie token
	function buildHiddenValues() {
		return {
			appointment_date: editDate,
			start_time: selectedSlot?.start_time ?? '',
			end_time: selectedSlot?.end_time ?? '',
			visit_type_code: editVisitType,
			chief_complaint: editComplaint
		};
	}

	const inp =
		'input w-full border-transparent bg-slate-100 text-main placeholder:text-main/30 focus:border-main focus:outline-none transition-colors';
	const sel =
		'select w-full border-transparent bg-slate-100 text-main focus:border-main focus:outline-none transition-colors';
	const lbl = 'label-text font-medium text-slate-500';
</script>

<!-- Edit Appointment Modal -->
{#if editingAppointment}
	<div
		class="fixed inset-0 z-50 flex items-center justify-center bg-black/50 p-4"
		transition:fade={{ duration: 200 }}
		role="presentation"
		onclick={closeEdit}
	>
		<div
			class="w-full max-w-lg overflow-hidden rounded-2xl bg-white shadow-2xl"
			transition:fly={{ y: 24, duration: 300, easing: cubicOut }}
			role="presentation"
			onclick={(e) => e.stopPropagation()}
		>
			<!-- Header -->
			<div class="flex items-center justify-between bg-main px-6 py-4">
				<div class="flex items-center gap-2">
					<Pencil size={16} class="text-text-main/80" />
					<h3 class="text-lg font-bold text-text-main">Edit Appointment</h3>
				</div>
				<button
					class="btn btn-circle text-text-main/80 btn-ghost btn-sm"
					onclick={closeEdit}
					aria-label="Close"
				>
					<X size={18} />
				</button>
			</div>

			<div class="flex flex-col gap-4 p-6">
				<!-- Current appointment summary -->
				<div class="flex items-center gap-3 rounded-xl bg-slate-50 px-4 py-3">
					<Stethoscope size={16} class="shrink-0 text-main/50" />
					<div>
						<p class="text-sm font-semibold text-main">{editingAppointment.service_name}</p>
						<p class="text-xs text-slate-400">
							Currently: {formatDate(editingAppointment.appointment_date)} ·
							{formatTime(editingAppointment.start_time)} – {formatTime(
								editingAppointment.end_time
							)}
						</p>
					</div>
				</div>

				<form
					method="POST"
					action="?/edit_appointment"
					use:enhance={() => {
						return async ({ result, update }) => {
							await update();
							if (result.type === 'redirect') closeEdit();
						};
					}}
					class="flex flex-col gap-4"
				>
					<input type="hidden" name="appointment_id" value={editingAppointment.id} />
					<input type="hidden" name="appointment_date" value={editDate} />
					<input
						type="hidden"
						name="start_time"
						value={selectedSlot?.start_time ?? editingAppointment.start_time}
					/>
					<input
						type="hidden"
						name="end_time"
						value={selectedSlot?.end_time ?? editingAppointment.end_time}
					/>
					<input type="hidden" name="visit_type_code" value={editVisitType} />
					<input type="hidden" name="chief_complaint" value={editComplaint} />

					<!-- Step 1: Pick a date -->
					<label class="form-control w-full">
						<div class="label pb-1"><span class={lbl}>Reschedule Date</span></div>
						<div class="flex gap-2">
							<input type="date" class="{inp} flex-1" min={today} bind:value={editDate} />
							<button
								type="button"
								class="btn border-none bg-main text-text-main hover:bg-sub disabled:opacity-50"
								disabled={!editDate || slotsLoading}
								onclick={fetchSlots}
							>
								{#if slotsLoading}
									<LoaderCircle size={16} class="animate-spin" />
								{:else}
									Check Slots
								{/if}
							</button>
						</div>
					</label>

					<!-- Step 2: Pick a slot -->
					{#if slotsError}
						<p
							class="rounded-lg bg-red-50 px-3 py-2 text-sm text-red-500"
							transition:slide={{ duration: 150 }}
						>
							{slotsError}
						</p>
					{/if}

					{#if slots.length > 0}
						<div transition:slide={{ duration: 200 }}>
							<div class="label pb-1"><span class={lbl}>Available Slots</span></div>
							<div class="grid grid-cols-3 gap-2 sm:grid-cols-4">
								{#each slots as slot (slot.start_time)}
									<button
										type="button"
										class="rounded-xl border px-3 py-2 text-sm font-medium transition-all
											{selectedSlot?.start_time === slot.start_time
											? 'border-main bg-main text-text-main shadow-sm'
											: 'border-slate-200 bg-slate-50 text-main hover:border-main hover:bg-main/5'}"
										onclick={() => (selectedSlot = slot)}
									>
										{formatTime(slot.start_time)}
									</button>
								{/each}
							</div>
							{#if selectedSlot}
								<p class="mt-2 text-xs text-main" transition:slide={{ duration: 150 }}>
									✓ {formatTime(selectedSlot.start_time)} – {formatTime(selectedSlot.end_time)} selected
								</p>
							{/if}
						</div>
					{/if}

					<!-- Visit Type -->
					<label class="form-control w-full">
						<div class="label pb-1"><span class={lbl}>Visit Type</span></div>
						<select class={sel} bind:value={editVisitType}>
							<option value="OPD">Out-Patient (OPD)</option>
							<option value="FOLLOW_UP">Follow-up</option>
							<option value="EMERGENCY">Emergency</option>
						</select>
					</label>

					<!-- Chief Complaint -->
					<label class="form-control w-full">
						<div class="label pb-1"><span class={lbl}>Chief Complaint</span></div>
						<textarea
							rows="3"
							class="textarea w-full border-transparent bg-slate-100 text-main transition-colors focus:border-main focus:outline-none"
							bind:value={editComplaint}
						></textarea>
					</label>

					<div class="flex gap-2">
						<button
							type="button"
							class="btn flex-1 border-main text-main btn-outline hover:bg-main hover:text-text-main"
							onclick={closeEdit}>Cancel</button
						>
						<button
							type="submit"
							class="btn flex-1 border-none bg-main text-text-main hover:bg-sub"
						>
							Save Changes
						</button>
					</div>
				</form>
			</div>
		</div>
	</div>
{/if}

<!-- Appointment Cards -->
<div class="flex flex-col gap-4">
	{#if active.length === 0}
		<div class="flex flex-col items-center gap-2 py-12 text-center">
			<CalendarDays size={36} class="text-main/20" />
			<p class="text-sm text-slate-500">No upcoming appointments.</p>
		</div>
	{:else}
		{#each active as appt (appt.id)}
			<div
				class="card bg-white shadow-sm transition-shadow hover:shadow-md"
				transition:slide={{ duration: 200 }}
			>
				<div class="card-body gap-3 p-4 sm:p-5">
					<div class="flex items-start justify-between gap-2">
						<div>
							<div class="flex items-center gap-1.5">
								<Stethoscope size={15} class="shrink-0 text-main/50" />
								<h3 class="font-semibold text-main">{appt.service_name}</h3>
							</div>
							<div class="mt-0.5 flex items-center gap-1 text-sm text-slate-500">
								<PawPrint size={12} class="shrink-0" />
								{appt.pet_name}
							</div>
						</div>
						<span
							class="badge shrink-0 capitalize
							{appt.status === 'confirmed' ? 'badge-success' : 'badge-warning'}"
						>
							{appt.status}
						</span>
					</div>

					<div class="grid grid-cols-2 gap-3 rounded-xl bg-slate-50 p-3">
						<div>
							<p class="flex items-center gap-1 text-xs text-slate-400">
								<CalendarDays size={11} /> Date
							</p>
							<p class="text-sm font-medium text-main">{formatDate(appt.appointment_date)}</p>
						</div>
						<div>
							<p class="flex items-center gap-1 text-xs text-slate-400">
								<Clock size={11} /> Time
							</p>
							<p class="text-sm font-medium text-main">
								{formatTime(appt.start_time)} — {formatTime(appt.end_time)}
							</p>
						</div>
						<div>
							<p class="text-xs text-slate-400">Visit Type</p>
							<p class="text-sm font-medium text-main">
								{visitLabels[appt.visit_type_code] ?? appt.visit_type_code}
							</p>
						</div>
						<div>
							<p class="flex items-center gap-1 text-xs text-slate-400">
								<AlertCircle size={11} /> Chief Complaint
							</p>
							<p class="truncate text-sm font-medium text-main">{appt.chief_complaint}</p>
						</div>
					</div>

					<div class="flex gap-2">
						<button
							class="btn flex-1 border-main text-main btn-outline btn-sm hover:bg-main hover:text-text-main"
							onclick={() => openEdit(appt)}
						>
							<Pencil size={13} /> Edit
						</button>
						<form method="POST" action="?/cancel_appointment" use:enhance class="flex-1">
							<input type="hidden" name="appointment_id" value={appt.id} />
							<button
								type="submit"
								class="btn w-full border-red-400 text-red-400 btn-outline btn-sm hover:bg-red-400 hover:text-white"
							>
								<X size={13} /> Cancel
							</button>
						</form>
					</div>
				</div>
			</div>
		{/each}
	{/if}
</div>
