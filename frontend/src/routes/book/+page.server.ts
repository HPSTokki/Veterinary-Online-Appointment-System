import { redirect } from "@sveltejs/kit";
import type { PageServerLoad } from "./$types";
import { getClientProfile } from "$lib/api/client";
import { getPets } from "$lib/api/pet";

export const load: PageServerLoad = async ({ locals }) => {
    if (!locals.user) redirect(303, '/')
    
    const profile = await getClientProfile(locals.token!)
    if (!profile) redirect(303, '/profile')

    const pets = await getPets(locals.token!)
    if (pets.length === 0) redirect(303, '/profile')

    redirect(303, '/appointment')
}