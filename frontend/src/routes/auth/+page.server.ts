import { fail, redirect } from "@sveltejs/kit";
import type { Actions } from "./$types";
import { loginUser, registerUser } from "$lib/api/auth";

export const actions: Actions = {
    login: async ({ request, cookies }) => {
        const form = await request.formData()
        const email = form.get('email') as string
        const password = form.get('password') as string

        try {
            const result = await loginUser({ email, password })
            cookies.set('token', result.access_token, {
                path: '/',
                httpOnly: true,
                sameSite: 'strict',
                maxAge: 60 * 30
            })
        } catch (error: any) {
            return fail(401, { message: error.message })
        }

        redirect(303, '/')

    },

    register: async ({ request, cookies }) => {
        const form = await request.formData()
        const email = form.get('email') as string
        const password = form.get('password') as string

        try {
            await registerUser({ email, password })
            const result = await loginUser({ email, password })
            cookies.set('token', result.access_token, {
                path: '/',
                httpOnly: true,
                sameSite: 'strict',
                maxAge: 60 * 30
            })
        } catch (error: any) {
            return fail(400, { message: error.message })
        }

        redirect(303, '/')

    }

}
