<script lang="ts">
    let { open = $bindable(false)} = $props();
    let mode = $state('false')
</script>

{#if open}
<dialog class="fixed inset-0 z-50 m-0 flex h-full w-full max-w-none items-center justify-center bg-black/50 p-0"
        onclick={() => open = false}
        aria-modal="true"
        open>
    <div class="w-full max-w-md rounded-xl bg-white p-6 shadow-xl"
         onclick={(e) => e.stopPropagation()} role="presentation">

        {#if mode === 'login'}
            <form class="fieldset w-full rounded-box border border-main bg-main p-4">
                <fieldset class="fieldset">
                    <label class="label" for="email">Email</label>
                    <input type="email" class="validator input bg-text-main text-slate-800" placeholder="Email" required />
                    <p class="validator-hint hidden">Required</p>
                </fieldset>
                <fieldset class="fieldset">
                    <label class="label" for="password">Password</label>
                    <input type="password" class="validator input bg-text-main text-slate-800" placeholder="Password" required />
                    <p class="validator-hint hidden">Required</p>
                </fieldset>
                <button class="btn mt-4 btn-neutral w-full" type="submit">Login</button>
                <button class="btn mt-1 btn-ghost w-full" type="reset">Reset</button>
            </form>
            <p class="mt-3 text-center text-sm">
                No account yet? 
                <button class="link" type="button" onclick={() => mode = 'register'}>Register here</button>
            </p>

        {:else}
            <form class="fieldset w-full rounded-box border border-main bg-main p-4">
                <fieldset class="fieldset">
                    <label class="label" for="email">Email</label>
                    <input type="email" class="validator input bg-text-main text-slate-800" placeholder="Email" required />
                    <p class="validator-hint hidden">Required</p>
                </fieldset>
                <fieldset class="fieldset">
                    <label class="label" for="password">Password</label>
                    <input type="password" class="validator input bg-text-main text-slate-800" placeholder="Password" required />
                    <p class="validator-hint hidden">Required</p>
                </fieldset>
                <button class="btn mt-4 btn-neutral w-full" type="submit">Register</button>
                <button class="btn mt-1 btn-ghost w-full" type="reset">Reset</button>
            </form>
            <p class="mt-3 text-center text-sm">
                Already have an account? 
                <button class="link" type="button" onclick={() => mode = 'login'}>Login here</button>
            </p>
        {/if}

        <button class="btn btn-ghost btn-sm mt-2 w-full" type="button" onclick={() => open = false}>
            Close
        </button>
    </div>
</dialog>
{/if}