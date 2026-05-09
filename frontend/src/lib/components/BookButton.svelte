<script lang="ts">
	import { page } from '$app/state';
	import { goto } from '$app/navigation';
	import { CalendarPlus } from '@lucide/svelte';
	import AuthModal from '$lib/components/AuthModal.svelte';

	let modalOpen = $state(false);

	function handleBook() {
		if (page.data.user) {
			goto('/book');
		} else {
			modalOpen = true;
		}
	}
</script>

<div class="fixed right-4 bottom-4 z-40 sm:right-6 sm:bottom-6">
	<button
		onclick={handleBook}
		class="btn gap-2 rounded-full border-none bg-main px-5 text-text-main shadow-lg hover:bg-sub sm:px-6"
	>
		<CalendarPlus size={18} />
		<span class="text-sm font-semibold">Book Appointment</span>
	</button>
</div>

<AuthModal bind:open={modalOpen} />
