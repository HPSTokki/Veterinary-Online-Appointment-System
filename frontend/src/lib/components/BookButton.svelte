<script lang="ts">
    import AuthModal from "$lib/components/AuthModal.svelte";
    let modalOpen = $state(false)
    
</script>

<div class="fixed bottom-6 right-6 z-40">
    <button onclick={() => modalOpen = true} 
            class="btn btn-primary rounded-full shadow-lg px-6">
        Book Appointment
    </button>
</div>
<AuthModal bind:open={modalOpen} />