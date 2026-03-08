<script lang="ts">
	import { enhance } from '$app/forms';

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
		return new Date(dt).toISOString().slice(0, 16);
	}

	function statusColor(status: string) {
		return status === 'confirmed' ? 'badge-success' : 'badge-warning';
	}
</script>

<!-- Edit Appointment Modal -->
{#if editingAppointment}
	<dialog
		class="fixed inset-0 z-50 flex items-center justify-center bg-black/50"
		aria-modal="true"
		onclick={() => (editingAppointment = null)}
	>
		<div
			class="w-full max-w-lg rounded-2xl bg-text-main! p-6 shadow-2xl"
			role="presentation"
			onclick={(e) => e.stopPropagation()}
		>
			<h3 class="mb-4 text-lg font-bold text-main!">Edit Appointment</h3>

			{#if editingAppointment}
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
						<div class="label"><span class="label-text font-medium text-main!">Date</span></div>
						<input
							type="date"
							name="appointment_date"
							class="input-bordered input w-full border-main! focus:outline-main!"
							value={editingAppointment.appointment_date.split('T')[0]}
						/>
					</label>

					<div class="grid grid-cols-2 gap-3">
						<label class="form-control w-full">
							<div class="label">
								<span class="label-text font-medium text-main!">Start Time</span>
							</div>
							<input
								type="datetime-local"
								name="start_time"
								class="input-bordered input w-full border-main! focus:outline-main!"
								value={toDatetimeLocal(editingAppointment.start_time)}
							/>
						</label>
						<label class="form-control w-full">
							<div class="label">
								<span class="label-text font-medium text-main!">End Time</span>
							</div>
							<input
								type="datetime-local"
								name="end_time"
								class="input-bordered input w-full border-main! focus:outline-main!"
								value={toDatetimeLocal(editingAppointment.end_time)}
							/>
						</label>
					</div>

					<label class="form-control w-full">
						<div class="label">
							<span class="label-text font-medium text-main!">Visit Type</span>
						</div>
						<select
							name="visit_type_code"
							class="select-bordered select w-full border-main! focus:outline-main!"
						>
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
						<div class="label">
							<span class="label-text font-medium text-main!">Chief Complaint</span>
						</div>
						<textarea
							name="chief_complaint"
							class="textarea-bordered textarea w-full border-main! focus:outline-main!"
							rows="3">{editingAppointment.chief_complaint}</textarea
						>
					</label>

					<div class="mt-2 flex gap-2">
						<button
							type="button"
							class="btn flex-1 border-main! text-main! btn-outline hover:bg-main! hover:text-text-main!"
							onclick={() => (editingAppointment = null)}
						>
							Cancel
						</button>
						<button
							type="submit"
							class="btn flex-1 border-none bg-main! text-text-main! hover:bg-sub!"
						>
							Save Changes
						</button>
					</div>
				</form>
			{/if}
		</div>
	</dialog>
{/if}

<!-- Appointment Cards -->
<div class="flex flex-col gap-4">
	{#if active.length === 0}
		<div class="py-8 text-center">
			<p class="mb-2 text-4xl">📋</p>
			<p class="text-sm text-main/60!">No upcoming appointments.</p>
		</div>
	{:else}
		{#each active as appt}
			<div
				class="card border border-main/20! bg-text-main! shadow-sm transition-shadow hover:shadow-md"
			>
				<div class="card-body gap-2 p-4">
					<!-- Header -->
					<div class="flex items-center justify-between">
						<div class="flex items-center gap-2">
							<h3 class="font-semibold text-main!">{appt.service_name}</h3>
							<span class="text-xs text-main/40!">·</span>
							<p class="text-sm text-main/60!">🐾 {appt.pet_name}</p>
						</div>
						<span class="badge {statusColor(appt.status)} text-xs capitalize">{appt.status}</span>
					</div>

					<!-- Details -->
					<div class="mt-1 grid grid-cols-2 gap-2">
						<div>
							<p class="text-xs text-main/50!">Date</p>
							<p class="text-sm font-medium text-main!">{formatDate(appt.appointment_date)}</p>
						</div>
						<div>
							<p class="text-xs text-main/50!">Time</p>
							<p class="text-sm font-medium text-main!">
								{formatTime(appt.start_time)} — {formatTime(appt.end_time)}
							</p>
						</div>
						<div>
							<p class="text-xs text-main/50!">Visit Type</p>
							<p class="text-sm font-medium text-main!">{appt.visit_type_code}</p>
						</div>
						<div>
							<p class="text-xs text-main/50!">Chief Complaint</p>
							<p class="truncate text-sm font-medium text-main!">{appt.chief_complaint}</p>
						</div>
					</div>

					<!-- Actions -->
					<div class="mt-2 flex gap-2">
						<button
							class="btn flex-1 border-main! text-main! btn-outline btn-sm hover:bg-main! hover:text-text-main!"
							onclick={() => (editingAppointment = appt)}
						>
							Edit
						</button>
						<form method="POST" action="?/cancel_appointment" use:enhance class="flex-1">
							<input type="hidden" name="appointment_id" value={appt.id} />
							<button
								type="submit"
								class="btn w-full border-red-400! text-red-400! btn-outline btn-sm hover:bg-red-400! hover:text-white!"
							>
								Cancel
							</button>
						</form>
					</div>
				</div>
			</div>
		{/each}
	{/if}
</div>