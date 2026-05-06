<script lang="ts">
    import { enhance } from '$app/forms'
    import { goto } from '$app/navigation'
    
    let { open = $bindable(false) } = $props()
    let mode = $state<'login' | 'register' | 'forgot' | 'reset'>('login')
    let showPasswordLogin = $state(false)
    let showPasswordRegister = $state(false)
    let showNewPassword = $state(false)

    let forgotEmail = $state('')
    let resetPin = $state('')
    let newPassword = $state('')
    let forgotError = $state<string | null>(null)
    let forgotSuccess = $state<string | null>(null)

    function resetState() {
        forgotEmail = ''
        resetPin = ''
        newPassword = ''
        forgotError = null
        forgotSuccess = null
    }
    
    function handleFocus(event: FocusEvent) {
        const target = event.target as HTMLElement
        target.classList.add('border-[#2F5D4E]')
        target.classList.remove('border-gray-300')
    }
    
    function handleBlur(event: FocusEvent) {
        const target = event.target as HTMLElement
        target.classList.add('border-gray-300')
        target.classList.remove('border-[#2F5D4E]')
    }
    
    // Handle login form submission
    async function handleLogin(event: Event) {
        event.preventDefault()
        const form = event.target as HTMLFormElement
        const formData = new FormData(form)
        
        const response = await fetch('/auth?/login', {
            method: 'POST',
            body: formData,
            headers: {
                'Accept': 'application/json'
            }
        })
        
        const result = await response.json()
        
        if (response.ok && result.success) {
            open = false // Close modal on success
            goto('/dashboard') // Or wherever you want to redirect
        } else {
            // Show error message (you can add an error state variable)
            console.error('Login failed:', result.error)
        }
    }
    
    // Handle register form submission
    async function handleRegister(event: Event) {
        event.preventDefault()
        const form = event.target as HTMLFormElement
        const formData = new FormData(form)
        
        const response = await fetch('/auth?/register', {
            method: 'POST',
            body: formData,
            headers: {
                'Accept': 'application/json'
            }
        })
        
        const result = await response.json()
        
        if (response.ok && result.success) {
            mode = 'login' // Switch to login mode after successful registration
            forgotSuccess = 'Account created! Please login.'
        } else {
            forgotError = result.error || 'Registration failed'
        }
    }
    
    // Handle forgot password form submission
    async function handleForgotPassword(event: Event) {
        event.preventDefault()
        const form = event.target as HTMLFormElement
        const formData = new FormData(form)
        
        forgotError = null
        forgotSuccess = null
        
        const response = await fetch('/auth?/forgot_password', {
            method: 'POST',
            body: formData,
            headers: {
                'Accept': 'application/json'
            }
        })
        
        const result = await response.json()
        
        if (response.ok && result.success) {
            forgotSuccess = result.message || 'PIN sent to your email!'
            setTimeout(() => {
                mode = 'reset' // Auto-switch to reset mode after success
            }, 2000)
        } else {
            forgotError = result.error || 'Failed to send PIN'
        }
    }
    
    // Handle reset password form submission
    async function handleResetPassword(event: Event) {
        event.preventDefault()
        const form = event.target as HTMLFormElement
        const formData = new FormData(form)
        
        forgotError = null
        
        const response = await fetch('/auth?/reset_password', {
            method: 'POST',
            body: formData,
            headers: {
                'Accept': 'application/json'
            }
        })
        
        const result = await response.json()
        
        if (response.ok && result.success) {
            mode = 'login'
            forgotSuccess = 'Password reset successfully! Please login.'
            resetState()
        } else {
            forgotError = result.error || 'Failed to reset password'
        }
    }
</script>

{#if open}
<dialog
    class="fixed inset-0 z-50 m-0 flex h-full w-full max-w-none items-center justify-center bg-black/60 p-4 border-none"
    onclick={() => open = false}
    aria-modal="true"
    open>
    <div class="w-full max-w-md rounded-2xl shadow-2xl overflow-hidden bg-white"
         role="presentation"
         onclick={(e) => e.stopPropagation()}>

        <!-- Header -->
        <div class="bg-[#2F5D4E] px-6 py-4 flex items-center justify-between">
            <div>
                <h2 class="text-[#F2F8F4] font-bold text-lg leading-tight">
                    {#if mode === 'login'}Welcome Back
                    {:else if mode === 'register'}Create Account
                    {:else if mode === 'forgot'}Forgot Password
                    {:else}Reset Password
                    {/if}
                </h2>
                <p class="text-[#F2F8F4]/70 text-xs mt-0.5">
                    Dr. Rosario Veterinary Clinic
                </p>
            </div>
            <button
                type="button"
                onclick={() => open = false}
                class="text-[#F2F8F4]/70 hover:opacity-100 transition-opacity text-xl leading-none">
                ✕
            </button>
        </div>

        <!-- Body -->
        <div class="px-6 py-6 flex flex-col gap-4 bg-white">

            <!-- ===== LOGIN ===== -->
            {#if mode === 'login'}
            <form onsubmit={handleLogin} class="flex flex-col gap-4">

                <div class="flex flex-col gap-1">
                    <label class="text-gray-900 text-sm font-medium">Email</label>
                    <input
                        name="email"
                        type="email"
                        placeholder="you@example.com"
                        required
                        class="bg-gray-50 text-gray-900 border border-gray-300 rounded-lg px-3 py-2.5 text-sm outline-none w-full focus:border-[#2F5D4E] transition-colors"
                        onfocus={handleFocus}
                        onblur={handleBlur}
                    />
                </div>

                <div class="flex flex-col gap-1">
                    <label class="text-gray-900 text-sm font-medium">Password</label>
                    <div class="relative">
                        <input
                            name="password"
                            type={showPasswordLogin ? 'text' : 'password'}
                            placeholder="••••••••"
                            required
                            class="bg-gray-50 text-gray-900 border border-gray-300 rounded-lg px-3 py-2.5 pr-10 text-sm outline-none w-full focus:border-[#2F5D4E] transition-colors"
                            onfocus={handleFocus}
                            onblur={handleBlur}
                        />
                        <button type="button"
                                class="absolute right-3 top-1/2 -translate-y-1/2 text-gray-500 hover:text-gray-700"
                                onclick={() => showPasswordLogin = !showPasswordLogin}>
                            {#if showPasswordLogin}
                                <svg xmlns="http://www.w3.org/2000/svg" class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13.875 18.825A10.05 10.05 0 0112 19c-4.478 0-8.268-2.943-9.543-7a9.97 9.97 0 011.563-3.029m5.858.908a3 3 0 114.243 4.243M9.878 9.878l4.242 4.242M9.88 9.88l-3.29-3.29m7.532 7.532l3.29 3.29M3 3l3.59 3.59m0 0A9.953 9.953 0 0112 5c4.478 0 8.268 2.943 9.543 7a10.025 10.025 0 01-4.132 4.411m0 0L21 21" />
                                </svg>
                            {:else}
                                <svg xmlns="http://www.w3.org/2000/svg" class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
                                </svg>
                            {/if}
                        </button>
                    </div>
                </div>

                <button
                    type="submit"
                    class="bg-[#2F5D4E] text-[#F2F8F4] border-none rounded-lg py-2.5 font-semibold text-sm cursor-pointer w-full hover:bg-[#2E6F40] transition-colors">
                    Login
                </button>
            </form>

            <div class="flex items-center justify-between text-sm text-gray-600">
                <button class="hover:underline text-[#2F5D4E] text-xs"
                        onclick={() => { mode = 'forgot'; resetState() }}>
                    Forgot Password?
                </button>
                <button class="hover:underline text-[#2F5D4E] text-xs"
                        onclick={() => mode = 'register'}>
                    No account? Register
                </button>
            </div>

            <!-- ===== REGISTER ===== -->
            {:else if mode === 'register'}
            <form onsubmit={handleRegister} class="flex flex-col gap-4">

                {#if forgotError}
                    <div class="bg-red-50 text-red-600 rounded-lg px-3 py-2.5 text-sm">
                        {forgotError}
                    </div>
                {/if}
                {#if forgotSuccess}
                    <div class="bg-green-50 text-green-600 rounded-lg px-3 py-2.5 text-sm">
                        {forgotSuccess}
                    </div>
                {/if}

                <div class="flex flex-col gap-1">
                    <label class="text-gray-900 text-sm font-medium">Email</label>
                    <input
                        name="email"
                        type="email"
                        placeholder="you@example.com"
                        required
                        class="bg-gray-50 text-gray-900 border border-gray-300 rounded-lg px-3 py-2.5 text-sm outline-none w-full focus:border-[#2F5D4E] transition-colors"
                        onfocus={handleFocus}
                        onblur={handleBlur}
                    />
                </div>

                <div class="flex flex-col gap-1">
                    <label class="text-gray-900 text-sm font-medium">Password</label>
                    <div class="relative">
                        <input
                            name="password"
                            type={showPasswordRegister ? 'text' : 'password'}
                            placeholder="••••••••"
                            required
                            class="bg-gray-50 text-gray-900 border border-gray-300 rounded-lg px-3 py-2.5 pr-10 text-sm outline-none w-full focus:border-[#2F5D4E] transition-colors"
                            onfocus={handleFocus}
                            onblur={handleBlur}
                        />
                        <button type="button"
                                class="absolute right-3 top-1/2 -translate-y-1/2 text-gray-500 hover:text-gray-700"
                                onclick={() => showPasswordRegister = !showPasswordRegister}>
                            {#if showPasswordRegister}
                                <svg xmlns="http://www.w3.org/2000/svg" class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13.875 18.825A10.05 10.05 0 0112 19c-4.478 0-8.268-2.943-9.543-7a9.97 9.97 0 011.563-3.029m5.858.908a3 3 0 114.243 4.243M9.878 9.878l4.242 4.242M9.88 9.88l-3.29-3.29m7.532 7.532l3.29 3.29M3 3l3.59 3.59m0 0A9.953 9.953 0 0112 5c4.478 0 8.268 2.943 9.543 7a10.025 10.025 0 01-4.132 4.411m0 0L21 21" />
                                </svg>
                            {:else}
                                <svg xmlns="http://www.w3.org/2000/svg" class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
                                </svg>
                            {/if}
                        </button>
                    </div>
                </div>

                <button
                    type="submit"
                    class="bg-[#2F5D4E] text-[#F2F8F4] border-none rounded-lg py-2.5 font-semibold text-sm cursor-pointer w-full hover:bg-[#2E6F40] transition-colors">
                    Create Account
                </button>
            </form>

            <div class="text-center text-sm">
                <button class="hover:underline text-[#2F5D4E] text-xs"
                        onclick={() => mode = 'login'}>
                    Already have an account? Login
                </button>
            </div>

            <!-- ===== FORGOT PASSWORD ===== -->
            {:else if mode === 'forgot'}

            {#if forgotError}
                <div class="bg-red-50 text-red-600 rounded-lg px-3 py-2.5 text-sm">
                    {forgotError}
                </div>
            {/if}
            {#if forgotSuccess}
                <div class="bg-green-50 text-green-600 rounded-lg px-3 py-2.5 text-sm">
                    {forgotSuccess}
                </div>
            {/if}

            <p class="text-gray-600 text-sm text-center">
                Enter your email and we'll send you a 6-digit PIN to reset your password.
            </p>

            <form onsubmit={handleForgotPassword} class="flex flex-col gap-4">
                <div class="flex flex-col gap-1">
                    <label class="text-gray-900 text-sm font-medium">Email</label>
                    <input
                        name="email"
                        type="email"
                        bind:value={forgotEmail}
                        placeholder="you@example.com"
                        required
                        class="bg-gray-50 text-gray-900 border border-gray-300 rounded-lg px-3 py-2.5 text-sm outline-none w-full focus:border-[#2F5D4E] transition-colors"
                        onfocus={handleFocus}
                        onblur={handleBlur}
                    />
                </div>
                <button
                    type="submit"
                    class="bg-[#2F5D4E] text-[#F2F8F4] border-none rounded-lg py-2.5 font-semibold text-sm cursor-pointer w-full hover:bg-[#2E6F40] transition-colors">
                    Send PIN
                </button>
            </form>

            <div class="flex flex-col gap-2">
                <button class="text-[#2F5D4E] text-xs hover:underline"
                        onclick={() => { mode = 'reset'; resetState() }}>
                    Already have a PIN? Enter it →
                </button>
                <button class="text-gray-500 text-xs hover:underline"
                        onclick={() => { mode = 'login'; resetState() }}>
                    ← Back to Login
                </button>
            </div>

            <!-- ===== RESET PASSWORD ===== -->
            {:else if mode === 'reset'}

            {#if forgotError}
                <div class="bg-red-50 text-red-600 rounded-lg px-3 py-2.5 text-sm">
                    {forgotError}
                </div>
            {/if}
            {#if forgotSuccess}
                <div class="bg-green-50 text-green-600 rounded-lg px-3 py-2.5 text-sm">
                    {forgotSuccess}
                </div>
            {/if}

            <form onsubmit={handleResetPassword} class="flex flex-col gap-4">
                <div class="flex flex-col gap-1">
                    <label class="text-gray-900 text-sm font-medium">Email</label>
                    <input
                        name="email"
                        type="email"
                        bind:value={forgotEmail}
                        placeholder="you@example.com"
                        required
                        class="bg-gray-50 text-gray-900 border border-gray-300 rounded-lg px-3 py-2.5 text-sm outline-none w-full focus:border-[#2F5D4E] transition-colors"
                        onfocus={handleFocus}
                        onblur={handleBlur}
                    />
                </div>

                <div class="flex flex-col gap-1">
                    <label class="text-gray-900 text-sm font-medium">6-Digit PIN</label>
                    <input
                        name="pin"
                        type="text"
                        bind:value={resetPin}
                        placeholder="000000"
                        maxlength="6"
                        required
                        class="bg-gray-50 text-gray-900 border border-gray-300 rounded-lg px-3 py-2.5 text-lg tracking-widest text-center outline-none w-full font-mono focus:border-[#2F5D4E] transition-colors"
                        onfocus={handleFocus}
                        onblur={handleBlur}
                    />
                </div>

                <div class="flex flex-col gap-1">
                    <label class="text-gray-900 text-sm font-medium">New Password</label>
                    <div class="relative">
                        <input
                            name="new_password"
                            type={showNewPassword ? 'text' : 'password'}
                            bind:value={newPassword}
                            placeholder="••••••••"
                            required
                            class="bg-gray-50 text-gray-900 border border-gray-300 rounded-lg px-3 py-2.5 pr-10 text-sm outline-none w-full focus:border-[#2F5D4E] transition-colors"
                            onfocus={handleFocus}
                            onblur={handleBlur}
                        />
                        <button type="button"
                                class="absolute right-3 top-1/2 -translate-y-1/2 text-gray-500 hover:text-gray-700"
                                onclick={() => showNewPassword = !showNewPassword}>
                            {showNewPassword ? '🙈' : '👁️'}
                        </button>
                    </div>
                </div>

                <button
                    type="submit"
                    class="bg-[#2F5D4E] text-[#F2F8F4] border-none rounded-lg py-2.5 font-semibold text-sm cursor-pointer w-full hover:bg-[#2E6F40] transition-colors">
                    Reset Password
                </button>
            </form>

            <button class="text-gray-500 text-xs hover:underline"
                    onclick={() => { mode = 'login'; resetState() }}>
                ← Back to Login
            </button>
            {/if}

        </div>
    </div>
</dialog>
{/if}