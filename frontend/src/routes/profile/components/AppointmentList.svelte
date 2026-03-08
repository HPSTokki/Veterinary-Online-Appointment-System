<script lang="ts">

    interface Appointment {
        id: number
        pet_name: string | null
        service_name: string | null
        appointment_date: string
        start_time: string
        end_time: string
        visit_type_code: string
        chief_complaint: string
        status: string
    }

    let { appointments }: { appointments: Appointment[] } = $props()

    const active = $derived(
        appointments
            .filter(a => ['pending', 'confirmed'].includes(a.status))
            .sort((a, b) => new Date(a.appointment_date).getTime() - new Date(b.appointment_date).getTime())
    )

    function formatDate(dt: string) {
        return new Date(dt).toLocaleDateString([], {
            weekday: 'short', year: 'numeric', month: 'short', day: 'numeric'
        })
    }

    function formatTime(dt: string) {
        return new Date(dt).toLocaleTimeString([], {
            hour: '2-digit', minute: '2-digit'
        })
    }

    function statusColor(status: string) {
        return status === 'confirmed' ? 'badge-success' : 'badge-warning'
    }

</script>

<div class="flex flex-col gap-4">
    {#if active.length === 0}
        <div class="text-center py-8">
            <p class="text-4xl mb-2">📋</p>
            <p class="text-sm text-main/60!">No upcoming appointments.</p>
        </div>
    {:else}
        {#each active as appt}
        <div class="card bg-text-main! border border-main/20! shadow-sm hover:shadow-md transition-shadow">
            <div class="card-body gap-2 p-4">
                <div class="flex items-center justify-between">
                    <div class="flex items-center gap-2">
                        <h3 class="font-semibold text-main!">{appt.service_name}</h3>
                        <span class="text-main/40! text-xs">·</span>
                        <p class="text-sm text-main/60!">🐾 {appt.pet_name}</p>
                    </div>
                    <span class="badge {statusColor(appt.status)} text-xs capitalize">{appt.status}</span>
                </div>

                <div class="grid grid-cols-2 gap-2 mt-1">
                    <div>
                        <p class="text-xs text-main/50!">Date</p>
                        <p class="text-sm font-medium text-main!">{formatDate(appt.appointment_date)}</p>
                    </div>
                    <div>
                        <p class="text-xs text-main/50!">Time</p>
                        <p class="text-sm font-medium text-main!">{formatTime(appt.start_time)} — {formatTime(appt.end_time)}</p>
                    </div>
                    <div>
                        <p class="text-xs text-main/50!">Visit Type</p>
                        <p class="text-sm font-medium text-main!">{appt.visit_type_code}</p>
                    </div>
                    <div>
                        <p class="text-xs text-main/50!">Chief Complaint</p>
                        <p class="text-sm font-medium text-main! truncate">{appt.chief_complaint}</p>
                    </div>
                </div>
            </div>
        </div>
        {/each}
    {/if}
</div>