import type { Handle } from "@sveltejs/kit";

export const handle: Handle = async ({ event, resolve }) => {
    const token = event.cookies.get('token')
    if (token) {
        try {
            const response = await fetch("http://localhost:8000", {
                headers: {
                    Authorization: `Bearer ${token}`
                }
            })
            if (response.ok) {
                const user = await response.json()
                event.locals.user = user
                event.locals.token = token
            }
        } catch (error) {
            console.log(error)
        }
    }
    return resolve(event)
}