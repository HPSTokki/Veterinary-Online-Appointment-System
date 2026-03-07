import type { Handle } from "@sveltejs/kit";

export const handle: Handle = async ({ event, resolve }) => {
    const token = event.cookies.get('token')
    if (token) {
        try {
            const response = await fetch("http://localhost:8000/user/me", {
                headers: {
                    Authorization: `Bearer ${token}`
                }
            })
            if (response.ok) {
                const user = await response.json()
                event.locals.user = user
                event.locals.token = token
                console.log('locals.user:', event.locals.user)
            }
        } catch (error) {
            console.log(error)
        }
    }
    return resolve(event)
}