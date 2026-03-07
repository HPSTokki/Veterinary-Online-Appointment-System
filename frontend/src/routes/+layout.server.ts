import type { LayoutServerLoad } from "./$types";

export const load: LayoutServerLoad = async ({ locals }) => {
    console.log('Our Token', locals.token)
    return {
        user: locals.user,
        token: locals.token
    }
}