import { redirect, fail } from "@sveltejs/kit";
import type { Actions, PageServerLoad } from "./$types";
import { getPets } from "$lib/api/pet";
import { createAppointment, getServices } from "$lib/api/appointment"; 

export const load: PageServerLoad = async ({ locals }) => {
    if (!locals.user) redirect(303, '/')
    
    const [pets, services] = await Promise.all([
        getPets(locals.token!),
        getServices()
    ])
    return { pets, services, token: locals.token }
}

export const actions: Actions = {
    book: async ({ request, locals }) => {
        const form = await request.formData()

        const body = {
            pet_id: parseInt(form.get('pet_id') as string),
            service_id: parseInt(form.get('service_id') as string),
            appointment_date: form.get('appointment_date') as string,
            start_time: form.get('start_time') as string,
            end_time: form.get('end_time') as string,
            visit_type_code: form.get('visit_type_code') as string,
            chief_complaint: form.get('chief_complaint') as string,
            booking_source: 'online',
            status: 'pending'
        }

        console.log('body', body)

        try {
            const result = await createAppointment(locals.token!, body)
            return { success: true, appointment: result }
        } catch (error: any) {
            return fail(400, { message: error.message })
        }
    }
}