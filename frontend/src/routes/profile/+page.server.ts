import { getClientProfile, createClientProfile, updateProfile } from "$lib/api/client";
import { createPet, deletePet, getPets, updatePet, type CreatePetData } from "$lib/api/pet";
import type { CreateProfileData, UpdateProfileData } from "$lib/api/client";
import { fail, redirect, type Actions } from "@sveltejs/kit";
import type { PageServerLoad } from "../auth/$types";
import { cancelAppointment, getAppointments, updateAppointment } from "$lib/api/appointment";

export const load: PageServerLoad = async ({ locals }) => {
    if (!locals.user) redirect(303, '/')
    const profile = await getClientProfile(locals.token!)

    const [pets, appointments] = profile
        ? await Promise.all([
            getPets(locals.token!),
            getAppointments(locals.token!)
        ])
        : [[], []]

    console.log(appointments)
    return { pets, appointments, profile }
}

export const actions: Actions = {
    create_profile: async ({ request, locals }) => {
        const form = await request.formData()
        const body: CreateProfileData = {
            full_name: form.get("full_name") as string,
            address: form.get("address") as string,
            mobile_no: form.get("mobile_no") as string | null || null,
            tel_no: form.get("tel_no") as string | null || null,
            preferred_contact_method: form.get("preferred_contact_method") as string
        }
        try {
            await createClientProfile(locals.token!, body)
        } catch (error: any) {
            return fail(400, { message: error.message })
        }
        redirect(303, '/profile')
    },
    update_profile: async ({ request, locals }) => {
        const form = await request.formData()
        const body: UpdateProfileData = {
            address: form.get('address') as string | null ?? undefined,
            mobile_no: form.get('mobile_no') as string | null | undefined,
            tel_no: form.get('tel_no') as string | null | undefined,
            preferred_contact_method: form.get('preferred_contact_method') as string | null ?? undefined
        }
        try {
            await updateProfile(locals.token!, body)
        } catch (error: any) {
            return fail(400, { message: error.message })
        }
        redirect(303, '/profile')
    },
    add_pet: async ({ request, locals }) => {
        const form = await request.formData()
        const body: CreatePetData = {
            name: form.get('name') as string,
            breed: form.get('breed') as string,
            species_type: form.get('species_type') as string,
            sex: form.get('sex') as string,
            date_of_birth: form.get('date_of_birth') as string,
            is_spayed_neutered: form.get('is_spayed_neutered') === 'true',
            weight_kg: form.get('weight_kg') ? parseFloat(form.get('weight_kg') as string) : null
        }
        try {
            await createPet(locals.token!, body)
        } catch (error: any) {
            return fail(400, { message: error.message })
        }
        redirect(303, '/profile')
    },
    cancel_appointment: async ({ request, locals }) => {
        const form = await request.formData()
        const id = form.get('appointment_id') as string

        try {
            await cancelAppointment(locals.token!, parseInt(id))
        } catch (error: any) {
            return fail(400, { message: error.message })
        }
        redirect(303, '/profile')
    },
    edit_appointment: async ({ request, locals }) => {
        const form = await request.formData()
        const id = parseInt(form.get('appointment_id') as string)

        const body = {
            appointment_date: form.get('appointment_date') as string || undefined,
            start_time: form.get('start_time') as string || undefined,
            end_time: form.get('end_time') as string || undefined,
            visit_type_code: form.get('visit_type_code') as string || undefined,
            chief_complaint: form.get('chief_complaint') as string || undefined,
        }

        try {
            await updateAppointment(locals.token!, id, body)
        } catch (error: any) {
            return fail(400, { message: error.message })
        }
        redirect(303, '/profile')
    },
    edit_pet: async ({ request, locals }) => {
        const form = await request.formData()
        const id = parseInt(form.get('pet_id') as string)

        const body = {
            is_spayed_neutered: form.get('is_spayed_neutered') === 'true',
            weight_kg: form.get('weight_kg') ? parseFloat(form.get('weight_kg') as string) : null
        }

        try {
            await updatePet(locals.token!, id, body)
        } catch (error: any) {
            return fail(400, { message: error.message })
        }
        redirect(303, '/profile')
    },

    delete_pet: async ({ request, locals }) => {
        const form = await request.formData()
        const id = parseInt(form.get('pet_id') as string)

        try {
            await deletePet(locals.token!, id)
        } catch (error: any) {
            return fail(400, { message: error.message })
        }
        redirect(303, '/profile')
    }
}
