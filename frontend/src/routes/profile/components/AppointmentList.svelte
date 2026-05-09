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
		AlertCircle
	} from '@lucide/svelte';

	interface Appointment {
		id: number;
		pet_name: string | null;
		service_name: string | null;
		appointment_date: string;
		start_time: string;
		end_time: string;
		visit_type_code: string;
		chief_complaint: string;
		status: string;
	}

	let { appointments }: { appointments: Appointment[] } = $props();
	let editingAppointment = $state<Appointment | null>(null);

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
	function toDatetimeLocal(dt: string) {
		const d = new Date(dt);
		const p = (n: number) => String(n).padStart(2, '0');
		return `${d.getFullYear()}-${p(d.getMonth() + 1)}-${p(d.getDate())}T${p(d.getHours())}:${p(d.getMinutes())}`;
	}

	function toDateLocal(dt: string) {
		const d = new Date(dt);
		const p = (n: number) => String(n).padStart(2, '0');
		return `${d.getFullYear()}-${p(d.getMonth() + 1)}-${p(d.getDate())}`;
	}

	const inp =
		'input w-full border-transparent bg-slate-100 text-main placeholder:text-main/30 focus:border-main focus:outline-none transition-colors';
	const sel =
		'select w-full border-transparent bg-slate-100 text-main focus:border-main focus:outline-none transition-colors';
	const lbl = 'label-text font-medium text-slate-500';

	const visitLabels: Record<string, string> = {
		OPD: 'Out-Patient',
		FOLLOW_UP: 'Follow-up',
		EMERGENCY: 'Emergency'
	};
</script>

<!-- Edit Appointment Modal -->
{#if editingAppointment}
	<div
		class="fixed inset-0 z-50 flex items-center justify-center bg-black/50 p-4"
		transition:fade={{ duration: 200 }}
		role="presentation"
		onclick={() => (editingAppointment = null)}
	>
		<div
			class="w-full max-w-lg overflow-hidden rounded-2xl bg-white shadow-2xl"
			transition:fly={{ y: 24, duration: 300, easing: cubicOut }}
			role="presentation"
			onclick={(e) => e.stopPropagation()}
		>
			<!-- Modal header -->
			<div class="flex items-center justify-between bg-main px-6 py-4">
				<div class="flex items-center gap-2">
					<Pencil size={16} class="text-text-main/80" />
					<h3 class="text-lg font-bold text-text-main">Edit Appointment</h3>
				</div>
				<button
					class="btn btn-circle text-text-main/80 btn-ghost btn-sm"
					onclick={() => (editingAppointment = null)}
					aria-label="Close"
				>
					<X size={18} />
				</button>
			</div>

			<div class="p-6">
				<form
					method="POST"
					action="?/edit_appointment"
					use:enhance={() => {
						return async ({ result, update }) => {
							await update();
							if (result.type === 'redirect') editingAppointment = null;
						};
					}}
					class="flex flex-col gap-3"
				>
					<input type="hidden" name="appointment_id" value={editingAppointment.id} />

					<label class="form-control w-full">
						<div class="label pb-1"><span class={lbl}>Date</span></div>
						<input
							type="date"
							name="appointment_date"
							class={inp}
							value={toDateLocal(editingAppointment.appointment_date)}
						/>
					</label>

					<div class="grid grid-cols-2 gap-3">
						<label class="form-control w-full">
							<div class="label pb-1"><span class={lbl}>Start Time</span></div>
							<input
								type="datetime-local"
								name="start_time"
								class={inp}
								value={toDatetimeLocal(editingAppointment.start_time)}
							/>
						</label>
						<label class="form-control w-full">
							<div class="label pb-1"><span class={lbl}>End Time</span></div>
							<input
								type="datetime-local"
								name="end_time"
								class={inp}
								value={toDatetimeLocal(editingAppointment.end_time)}
							/>
						</label>
					</div>

					<label class="form-control w-full">
						<div class="label pb-1"><span class={lbl}>Visit Type</span></div>
						<select name="visit_type_code" class={sel}>
							<option value="OPD" selected={editingAppointment.visit_type_code === 'OPD'}
								>Out-Patient (OPD)</option
							>
							<option
								value="FOLLOW_UP"
								selected={editingAppointment.visit_type_code === 'FOLLOW_UP'}>Follow-up</option
							>
							<option
								value="EMERGENCY"
								selected={editingAppointment.visit_type_code === 'EMERGENCY'}>Emergency</option
							>
						</select>
					</label>

					<label class="form-control w-full">
						<div class="label pb-1"><span class={lbl}>Chief Complaint</span></div>
						<textarea
							name="chief_complaint"
							rows="3"
							class="textarea w-full border-transparent bg-slate-100 text-main transition-colors focus:border-main focus:outline-none"
							>{editingAppointment.chief_complaint}</textarea
						>
					</label>

					<div class="mt-1 flex gap-2">
						<button
							type="button"
							class="btn flex-1 border-main text-main btn-outline hover:bg-main hover:text-text-main"
							onclick={() => (editingAppointment = null)}>Cancel</button
						>
						<button type="submit" class="btn flex-1 border-none bg-main text-text-main hover:bg-sub"
							>Save Changes</button
						>
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
					<!-- Header row -->
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

					<!-- Details grid -->
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

					<!-- Actions -->
					<div class="flex gap-2">
						<button
							class="btn flex-1 border-main text-main btn-outline btn-sm hover:bg-main hover:text-text-main"
							onclick={() => (editingAppointment = appt)}
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
