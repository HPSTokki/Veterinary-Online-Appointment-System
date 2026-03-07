<script lang="ts">
    import { enhance } from '$app/forms'
    let { data, form } = $props()
    let editing = $state(false)
    let addingPet = $state(false)
    let isNew = $derived(!data.profile)
</script>

<!-- ===== FIRST TIME: Profile Creation Modal ===== -->
{#if isNew}
<div class="fixed inset-0 z-50 flex items-center justify-center bg-black/60">
    <div class="w-full max-w-lg rounded-2xl bg-text-main p-6 shadow-2xl">
        <h2 class="mb-1 text-xl font-bold text-main!">Complete Your Profile</h2>
        <p class="mb-4 text-sm text-gray-500">Required before booking an appointment.</p>

        {#if form?.message}
            <div class="alert mb-3 text-sm bg-red-100! text-red-700!">{form.message}</div>
        {/if}

        <form method="POST" action="?/create_profile" use:enhance class="flex flex-col gap-3">
            <label class="form-control w-full">
                <div class="label"><span class="label-text text-main! font-medium">Full Name</span></div>
                <input type="text" name="full_name" class="input input-bordered w-full border-main! focus:outline-main!" placeholder="Juan Dela Cruz" required />
            </label>

            <label class="form-control w-full">
                <div class="label"><span class="label-text text-main! font-medium">Address</span></div>
                <input type="text" name="address" class="input input-bordered w-full border-main1 focus:outline-main!" placeholder="123 Mabini St., Bulacan" required />
            </label>

            <div class="grid grid-cols-2 gap-3">
                <label class="form-control w-full">
                    <div class="label"><span class="label-text text-main! font-medium">Mobile No.</span></div>
                    <input type="tel" name="mobile_no" class="input input-bordered w-full border-main! focus:outline-main!" placeholder="09XX XXX XXXX" />
                </label>
                <label class="form-control w-full">
                    <div class="label"><span class="label-text text-main! font-medium">Telephone No.</span></div>
                    <input type="tel" name="tel_no" class="input input-bordered w-full border-main! focus:outline-main!" placeholder="(044) XXX XXXX" />
                </label>
            </div>

            <label class="form-control w-full">
                <div class="label"><span class="label-text text-main! font-medium">Preferred Contact</span></div>
                <select name="preferred_contact_method" class="select select-bordered w-full border-main! focus:outline-main!">
                    <option value="Mobile No.">Mobile No.</option>
                    <option value="Telephone No.">Telephone No.</option>
                    <option value="Email">Email</option>
                </select>
            </label>

            <button type="submit" class="btn mt-2 w-full bg-main! text-text-main! hover:bg-sub! border-none">
                Save & Continue
            </button>
        </form>
    </div>
</div>

{:else}
<!-- ===== EXISTING PROFILE ===== -->
<div class="mx-auto max-w-3xl p-6 flex flex-col gap-8">

    <!-- Profile Section -->
    <div>
        <div class="flex items-center justify-between mb-4">
            <h2 class="text-2xl font-bold text-main!">My Profile</h2>
            <button class="btn btn-outline btn-sm border-main! text-main! hover:bg-main! hover:text-text-main!" 
                    onclick={() => editing = !editing}>
                {editing ? 'Cancel' : 'Edit'}
            </button>
        </div>

        {#if form?.message}
            <div class="alert mb-4 text-sm bg-red-100! text-red-700!">{form.message}</div>
        {/if}

        {#if !editing}
        <div class="card bg-text-main! shadow-sm border border-main/20!">
            <div class="card-body grid grid-cols-2 gap-4">
                {#each [
                    { label: 'Full Name', value: data.profile.full_name },
                    { label: 'Email', value: data.profile.email },
                    { label: 'Mobile No.', value: data.profile.mobile_no ?? '—' },
                    { label: 'Telephone No.', value: data.profile.tel_no ?? '—' },
                    { label: 'Preferred Contact', value: data.profile.preferred_contact_method },
                    { label: 'Address', value: data.profile.address },
                ] as field}
                <div>
                    <p class="text-xs text-main/60!">{field.label}</p>
                    <p class="font-medium text-main!">{field.value}</p>
                </div>
                {/each}
            </div>
        </div>

        {:else}
        <form method="POST" action="?/update_profile" use:enhance 
              class="card bg-text-main! shadow-sm border border-main/20!">
            <div class="card-body flex flex-col gap-3">
                <label class="form-control  w-full">
                    <div class="label"><span class="label-text text-main! font-medium">Address</span></div>
                    <input type="text" name="address" class="input input-bordered bg-text-main w-full border-main! focus:outline-main!" value={data.profile.address} />
                </label>
                <div class="grid grid-cols-2 gap-3">
                    <label class="form-control w-full">
                        <div class="label"><span class="label-text text-main! font-medium">Mobile No.</span></div>
                        <input type="tel" name="mobile_no" class="input bg-text-main input-bordered w-full border-main! focus:outline-main!" value={data.profile.mobile_no ?? ''} />
                    </label>
                    <label class="form-control w-full">
                        <div class="label"><span class="label-text text-main! font-medium">Telephone No.</span></div>
                        <input type="tel" name="tel_no" class="input bg-text-main input-bordered w-full border-main! focus:outline-main!" value={data.profile.tel_no ?? ''} />
                    </label>
                </div>
                <label class="form-control w-full">
                    <div class="label"><span class="label-text text-main! font-medium">Preferred Contact</span></div>
                    <select name="preferred_contact_method" class="select bg-text-main select-bordered w-full border-main! focus:outline-main!">
                        <option value="Mobile No." selected={data.profile.preferred_contact_method === 'Mobile No.'}>Mobile No.</option>
                        <option value="Telephone No." selected={data.profile.preferred_contact_method === 'Telephone No.'}>Telephone No.</option>
                        <option value="Email" selected={data.profile.preferred_contact_method === 'Email'}>Email</option>
                    </select>
                </label>
                <button type="submit" class="btn w-full bg-main! text-text-main! hover:bg-sub! border-none">
                    Update Profile
                </button>
            </div>
        </form>
        {/if}
    </div>

    <!-- Pets Section -->
    <div>
        <div class="flex items-center justify-between mb-4">
            <h2 class="text-2xl font-bold text-main!">My Pets</h2>
            <button class="btn btn-sm bg-main! text-text-main! hover:bg-sub! border-none" 
                    onclick={() => addingPet = !addingPet}>
                {addingPet ? 'Cancel' : '+ Add Pet'}
            </button>
        </div>

        {#if addingPet}
        <form method="POST" action="?/add_pet"
              use:enhance={() => {
                  return async ({ result, update }) => {
                      await update()
                      if (result.type === 'redirect' || result.type === 'success') {
                          addingPet = false
                      }
                  }
              }}
              class="card bg-text-main! shadow-sm border border-main/20! mb-4">
            <div class="card-body flex flex-col gap-3">
                <h3 class="font-semibold text-lg text-main!">New Pet</h3>

                <div class="grid grid-cols-2 gap-3">
                    <label class="form-control w-full">
                        <div class="label"><span class="label-text text-main! font-medium">Pet Name</span></div>
                        <input type="text" name="name" class="input bg-text-main input-bordered w-full border-main! focus:outline-main!" placeholder="Buddy" required />
                    </label>
                    <label class="form-control w-full">
                        <div class="label"><span class="label-text text-main! font-medium">Species</span></div>
                        <select name="species_type" class="select bg-text-main select-bordered w-full border-main! focus:outline-main!" required>
                            <option value="" disabled selected>Select</option>
                            <option value="Dog">Dog</option>
                            <option value="Cat">Cat</option>
                            <option value="Other">Other</option>
                        </select>
                    </label>
                    <label class="form-control w-full">
                        <div class="label"><span class="label-text text-main! font-medium">Breed</span></div>
                        <input type="text" name="breed" class="input bg-text-main input-bordered w-full border-main! focus:outline-main!" placeholder="Labrador" required />
                    </label>
                    <label class="form-control w-full">
                        <div class="label"><span class="label-text text-main! font-medium">Sex</span></div>
                        <select name="sex" class="select bg-text-main select-bordered w-full border-main! focus:outline-main!" required>
                            <option value="" disabled selected>Select</option>
                            <option value="Male">Male</option>
                            <option value="Female">Female</option>
                        </select>
                    </label>
                    <label class="form-control w-full">
                        <div class="label"><span class="label-text text-main! font-medium">Date of Birth</span></div>
                        <input type="date" name="date_of_birth" class="input bg-text-main input-bordered w-full border-main! focus:outline-main!" required />
                    </label>
                    <label class="form-control w-full">
                        <div class="label"><span class="label-text text-main! font-medium">Weight (kg)</span></div>
                        <input type="number" name="weight_kg" class="input bg-text-main input-bordered w-full border-main! focus:outline-main!" placeholder="4.5" step="0.1" min="0" />
                    </label>
                </div>

                <label class="flex items-center gap-2 cursor-pointer">
                    <input type="checkbox" name="is_spayed_neutered" value="true" class="checkbox checkbox-sm border-main! checked:bg-main!" />
                    <span class="label-text text-main!">Spayed / Neutered</span>
                </label>

                <button type="submit" class="btn w-full bg-main! text-text-main! hover:bg-sub! border-none">
                    Add Pet
                </button>
            </div>
        </form>
        {/if}

        {#if data.pets.length === 0}
            <div class="text-center py-8">
                <p class="text-4xl mb-2">🐾</p>
                <p class="text-sm text-main/60!">No pets added yet. Add your first pet above.</p>
            </div>
        {:else}
            <div class="grid grid-cols-1 gap-4 sm:grid-cols-2">
                {#each data.pets as pet}
                <div class="card bg-text-main! shadow-sm border border-main/20! hover:shadow-md transition-shadow">
                    <div class="card-body gap-1">
                        <div class="flex items-center justify-between">
                            <h3 class="card-title text-base text-main!">{pet.name}</h3>
                            <span class="badge badge-outline text-xs border-main! text-main!">{pet.species_type}</span>
                        </div>
                        <p class="text-sm text-main/70!">{pet.breed} · {pet.sex}</p>
                        <p class="text-xs text-main/50!">Born: {new Date(pet.date_of_birth).toLocaleDateString()}</p>
                        {#if pet.weight_kg}
                            <p class="text-xs text-main/50!">Weight: {pet.weight_kg} kg</p>
                        {/if}
                        <p class="text-xs text-main/50!">
                            {pet.is_spayed_neutered ? '✓ Spayed/Neutered' : '✗ Not Spayed/Neutered'}
                        </p>
                    </div>
                </div>
                {/each}
            </div>
        {/if}
    </div>

</div>
{/if}