<script lang="ts">
    import { page } from "$app/state";
    import { goto } from "$app/navigation";
    import AuthModal from "$lib/components/AuthModal.svelte";
    
    let modalOpen = $state(false)
    
    function handleBook() {
        if (page.data.user) {
            goto('/book')
        } else {
            modalOpen = true
        }
    }

</script>

<div class="fixed bottom-6 right-6 z-40">
    <button onclick={handleBook} 
            class="btn btn-primary bg-main! rounded-full shadow-lg px-6">
        Book Appointment
    </button>
</div>
<AuthModal bind:open={modalOpen} />